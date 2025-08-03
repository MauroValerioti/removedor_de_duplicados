import os
import shutil
from PIL import Image
import imagehash

# Check if the file is considered garbage based on its name
def is_garbage_file(filename):
    name, ext = os.path.splitext(filename.lower())
    return (
        name.endswith("thumb") or    # Ends with "thumb"
        "(1)" in name                # Has "(1)" in the name
    ) and ext in [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"]  # Only for image files

# Generate a perceptual hash (pHash) for the given image
def get_phash(image_path):
    try:
        with Image.open(image_path) as img:
            img = img.convert('RGB')             # Normalize colors
            return imagehash.phash(img)          # Return the pHash
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None  # Return None if something fails

# Main function to detect and move duplicate or garbage images
def move_duplicate_images(folder_path, threshold=5):
    hashes = {}               # Dictionary to store unique hashes
    moved_files = []          # List of visually similar images moved
    moved_garbage = []        # List of garbage files moved
    total_files_read = 0      # Counter of valid image files processed

    # Create a subfolder named "__DUPLICATES" inside the target folder
    duplicates_folder = os.path.join(folder_path, "__DUPLICATES")
    os.makedirs(duplicates_folder, exist_ok=True)

    # Walk through all files in the target folder (recursively)
    for root, _, files in os.walk(folder_path):
        for filename in files:
            filepath = os.path.join(root, filename)

            # Skip files already in the __DUPLICATES folder (to avoid infinite loop)
            if duplicates_folder in filepath:
                continue

            # Step 1: Handle garbage images
            if is_garbage_file(filename):
                try:
                    target_path = os.path.join(duplicates_folder, filename)
                    shutil.move(filepath, target_path)           # Move to __DUPLICATES
                    moved_garbage.append(target_path)            # Log it
                    print(f"🗑️ Moved garbage file: {filepath}")
                except Exception as e:
                    print(f"Could not move garbage: {filepath}: {e}")
                continue  # Skip to the next file

            # Step 2: Handle normal images (check for duplicates)
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp')):
                total_files_read += 1
                img_hash = get_phash(filepath)   # Generate perceptual hash
                if img_hash:
                    found_duplicate = False

                    # Compare with existing hashes
                    for existing_hash in hashes:
                        distance = img_hash - existing_hash  # Hamming distance
                        if distance <= threshold:
                            try:
                                target_path = os.path.join(duplicates_folder, filename)
                                shutil.move(filepath, target_path)     # Move duplicate
                                moved_files.append(target_path)        # Log it
                                found_duplicate = True
                                print(f"📦 Moved visually similar image: {filepath} (Distance: {distance})")
                                break  # No need to check other hashes
                            except Exception as e:
                                print(f"Could not move {filepath}: {e}")
                    if not found_duplicate:
                        # If no match was found, store this hash
                        hashes[img_hash] = filepath

    # Step 3: Save a log of moved files
    log_path = os.path.join(folder_path, "moved_images.txt")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("=== Garbage Files Moved ===\n")
        for fpath in moved_garbage:
            f.write(fpath + "\n")
        f.write("\n=== Duplicate Files Moved ===\n")
        for fpath in moved_files:
            f.write(fpath + "\n")

    # Step 4: Print final summary
    print("\n📊 Summary:")
    print(f"Garbage files moved: {len(moved_garbage)}")
    print(f"Valid images read: {total_files_read}")
    print(f"Visually similar images moved: {len(moved_files)}")
    print(f"Images remaining in original folder: {total_files_read - len(moved_files)}")
    print(f"Log saved to: {log_path}")

# Entry point of the script
if __name__ == "__main__":
    current_folder = os.path.dirname(os.path.abspath(__file__))  # Get folder where this script is located
    move_duplicate_images(current_folder, threshold=5)           # Start the process
