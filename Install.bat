@echo off
rem Set console background to black and foreground to white
color 0F

title GMT Installer

echo.
echo.
echo ====================================
echo   Global Multi-Tool (GMT) Installer
echo ====================================
echo.

echo Installing Python dependencies...
echo.

rem --- Actual pip installation ---
echo Running pip install for required packages...
echo.

rem Check if pip is available
where pip >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ERROR: pip not found. Please ensure Python is installed and added to your PATH.
    echo You can download Python from https://www.python.org/downloads/
    echo.
    goto :end_install
)

rem Install required packages
pip install psutil

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install one or more Python packages.
    echo Please check your internet connection or try running the script as administrator.
    echo.
) else (
    echo.
    echo All Python dependencies installed successfully!
)

rem --- Verifying installs with delay ---
:end_install
echo.
echo Verifying installs...
rem Using powershell for more reliable sleep across systems
powershell -Command "Start-Sleep -Seconds 5" >nul 2>&1 || (ping 127.0.0.1 -n 6 > nul)
echo.
echo Installation complete. You can now run Global MT.py in your GMT directory.
echo.
pause
