@echo off
echo Running duplicate image remover...

REM Activate Python if it's on PATH
REM Otherwise you can replace 'python' with full path to python.exe
python "%~dp0remove_duplicates.py"

echo.
echo ✅ Done. Press any key to exit.
pause >nul
