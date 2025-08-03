import os
import cv2
import shutil
import imagehash
from PIL import Image

# Extract 3 keyframes from the video at 10%, 50%, and 90% positions
def get_video_keyframes(video_path):
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"⚠️ Could not open {video_path}")
            return None

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_hashes = []
        frame_indexes = []

        # If too short, just take middle frame
        if total_frames < 30:
            frame_indexes = [int(total_frames * 0.5)]
        else:
            frame_indexes = [
                int(total_frames * 0.1),
                int(total_frames * 0.5),
                int(total_frames * 0.9)
            ]

        # Read each keyframe and hash it
        for idx in frame_indexes:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            if ret:
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(img)
                hash_val = imagehash.phash(pil_img)
                frame_hashes.append(hash_val)
            else:
                print(f"❌ Failed to read frame {idx} from {video_path}")
                return None

        cap.release()
        return frame_hashes

    except Exception as e:
        print(f"🔥 Error processing {video_path}: {e}")
        return None

# Main function to detect and move duplicate videos
def move_duplicate_videos(folder_path, threshold=5):
    video_extensions = ('.mp4', '.mov', '.avi', '.mkv')
    video_hashes = []              # Store keyframe hashes of each unique video
    moved_videos = []              # Store paths of moved duplicate videos
    total_videos = 0               # Count how many video files were scanned

    # Create destination folder for duplicates
    duplicates_folder = os.path.join(folder_path, "__DUPLICATE_VIDEOS")
    os.makedirs(duplicates_folder, exist_ok=True)

    # Walk through the current folder (not recursive)
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(video_extensions):
            filepath = os.path.join(folder_path, filename)

            # Skip files already in the duplicates folder
            if duplicates_folder in filepath:
                continue

            total_videos += 1
            keyframe_hashes = get_video_keyframes(filepath)

            if keyframe_hashes is None or len(keyframe_hashes) == 0:
                continue

            is_duplicate = False

            # Compare this video's keyframe hashes to all previously seen ones
            for existing_hashes in video_hashes:
                if len(existing_hashes) != len(keyframe_hashes):
                    continue

                # Compute distance for all 3 frames
                distances = [h1 - h2 for h1, h2 in zip(existing_hashes, keyframe_hashes)]

                # If all frames are visually similar, it's a duplicate
                if all(d <= threshold for d in distances):
                    is_duplicate = True
                    break

            if is_duplicate:
                try:
                    target_path = os.path.join(duplicates_folder, filename)
                    shutil.move(filepath, target_path)
                    moved_videos.append(target_path)
                    print(f"📦 Moved duplicate video: {filepath}")
                except Exception as e:
                    print(f"❌ Could not move {filepath}: {e}")
            else:
                video_hashes.append(keyframe_hashes)

    # Save a log of moved videos
    log_path = os.path.join(folder_path, "moved_videos.txt")
    with open(log_path, "w", encoding="utf-8") as f:
        for fpath in moved_videos:
            f.write(fpath + "\n")

    # Final summary output
    print("\n📊 Summary:")
    print(f"Videos scanned: {total_videos}")
    print(f"Duplicates moved: {len(moved_videos)}")
    print(f"Remaining videos: {total_videos - len(moved_videos)}")
    print(f"Moved video log: {log_path}")

# Entry point
if __name__ == "__main__":
    current_folder = os.path.dirname(os.path.abspath(__file__))  # Get folder where the script is
    move_duplicate_videos(current_folder, threshold=5)
