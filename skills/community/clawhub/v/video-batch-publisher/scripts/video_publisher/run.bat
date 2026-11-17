@echo off
chcp 65001 > nul
echo Launching video publisher...
echo ==============================
set "SYS_PYTHON=C:\Users\chenc\AppData\Local\Microsoft\WindowsApps\python.exe"
if not exist "%SYS_PYTHON%" (
    echo [错误] 未找到系统 Python：%SYS_PYTHON%
    pause
    exit /b 1
)
"%SYS_PYTHON%" "publisher_gui.py"
echo ==============================
echo Tool exited!
pause
