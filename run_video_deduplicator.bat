@echo off
echo Looking for duplicate videos in this folder...
python "%~dp0remove_video_duplicates.py"
echo.
echo ✅ Done. Press any key to exit.
pause >nul
