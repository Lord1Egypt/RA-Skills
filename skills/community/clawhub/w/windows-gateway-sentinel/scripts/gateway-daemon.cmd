@echo off
rem ============================================================
rem  OpenClaw Gateway watchdog (generic v2, Windows)
rem  Loop: sanitize env -> quarantine stale sqlite snapshots ->
rem        run gateway -> on exit kill zombie listeners -> retry 30s
rem  Stop cleanly: create file  gateway-daemon.stop  next to this script
rem  Configure via env vars before launching:
rem    OPENCLAW_DIR  (default C:\OpenClaw)
rem    OPENCLAW_PORT (default 18789)
rem ============================================================
setlocal
set "NODE_DIR=C:\Program Files\nodejs"
set "NPM_DIR=%APPDATA%\npm"
set "PATH=%NODE_DIR%;%NPM_DIR%;%PATH%"
if "%OPENCLAW_DIR%"=="" set "OPENCLAW_DIR=C:\OpenClaw"
if "%OPENCLAW_PORT%"=="" set "OPENCLAW_PORT=18789"
set "NO_PROXY=127.0.0.1,localhost,::1,registry.ollama.ai,ollama.ai"
set "no_proxy=%NO_PROXY%"
set "OCLOG=%OPENCLAW_DIR%\gateway-daemon.log"
set "OCSTOP=%OPENCLAW_DIR%\gateway-daemon.stop"
set "OCQ=%OPENCLAW_DIR%\_oc_snapshot_quarantine"
set "OCPORT=%OPENCLAW_PORT%"

rem ---- strip host-injected pollution (defense in depth) ----
set "NODE_OPTIONS="
set "PYTHONPATH="
set "BASH_ENV="
set "NODE_REPL_EXTERNAL_MODULE="
set "GENIE_TRASH_DIR="
for /f "tokens=1 delims==" %%V in ('set CODEBUDDY_ 2^>nul') do set "%%V="

rem ---- heap headroom (pressure restarts seen below ~1.4GB heap) ----
set "NODE_OPTIONS=--max-old-space-size=3072"

if not exist "%OCQ%" mkdir "%OCQ%" >nul 2>&1
echo [%DATE% %TIME%] daemon boot >> "%OCLOG%"

:loop
if exist "%OCSTOP%" (
  echo [%DATE% %TIME%] stop flag detected; daemon exiting >> "%OCLOG%"
  del /f /q "%OCSTOP%" >nul 2>&1
  exit /b 0
)

echo [%DATE% %TIME%] quarantine stale sqlite snapshots >> "%OCLOG%"
powershell -NoProfile -ExecutionPolicy Bypass -Command "$q='%OCQ%'; $r=Join-Path $env:LOCALAPPDATA 'openclaw'; if(Test-Path $r){ Get-ChildItem -LiteralPath $r -Directory -Filter 'openclaw-sqlite-readonly-*' -ErrorAction SilentlyContinue | ForEach-Object { try { Move-Item -LiteralPath $_.FullName -Destination $q -Force -ErrorAction Stop } catch {} } }" >> "%OCLOG%" 2>&1

echo [%DATE% %TIME%] starting: openclaw gateway run >> "%OCLOG%"
call openclaw gateway run >> "%OCLOG%" 2>&1
echo [%DATE% %TIME%] gateway exited rc=%ERRORLEVEL%; killing stale listener; restart in 30s >> "%OCLOG%"

rem ---- kill zombie listener left by restart_close_failed ----
for /f "tokens=5" %%P in ('netstat -ano ^| findstr ":%OCPORT%" ^| findstr "LISTENING"') do (
  echo [%DATE% %TIME%] killing zombie listener pid %%P on port %OCPORT% >> "%OCLOG%"
  taskkill /F /PID %%P >nul 2>&1
)

ping -n 31 127.0.0.1 >nul
goto loop
