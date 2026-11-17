@echo off
chcp 65001 >nul
echo WorkBuddy data migration (universal)
echo This moves your WorkBuddy data folder off the system drive to another fixed disk.
echo Close WorkBuddy fully (tray icon too), then press any key to start.
pause
set "NODE=%USERPROFILE%\.workbuddy\binaries\node\versions\22.22.2\node.exe"
if not exist "%NODE%" (
  echo Cannot find bundled node.exe at %NODE%
  echo Run this on a machine with WorkBuddy installed.
  pause
  exit /b 1
)
C:\Windows\System32\robocopy.exe "%USERPROFILE%\.workbuddy\binaries\node\versions\22.22.2" "C:\migrate_tmp" node.exe /R:1 /W:1 /NP >nul
if not exist "C:\migrate_tmp\node.exe" (
  echo FAILED to stage node.exe - aborting.
  pause
  exit /b 1
)
C:\migrate_tmp\node.exe "%~dp0migrate.js"
set RC=%errorlevel%
C:\Windows\System32\cmd.exe /c rmdir /s /q C:\migrate_tmp >nul 2>&1
echo.
if %RC%==0 (echo MIGRATION DONE OK - see log on the target drive root) else (echo MIGRATION HAD ERRORS - check the log)
pause
