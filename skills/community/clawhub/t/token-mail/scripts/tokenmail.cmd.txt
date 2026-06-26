@echo off
setlocal
set SCRIPT_DIR=%~dp0
where node >nul 2>nul
if not %errorlevel%==0 (
  echo Node.js not found. Please install Node.js 18+ first.
  exit /b 1
)
node "%SCRIPT_DIR%tokenmail_cli.js" %*
exit /b %errorlevel%
