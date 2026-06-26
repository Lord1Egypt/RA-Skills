# Install SeekDB — Windows MSI

**Supported systems:** Windows 10 (22H2+), Windows 11, Windows Server 2022+ (x86_64 only)
**Requirements:** 1-core CPU, 2 GB RAM, MySQL client installed, Administrator privileges for service registration.

> **Important agent note:** The seekdb MSI bundles a GUI configurator (`seekdbConfigurator.exe`) that **cannot** be automated by a CLI agent. The agent should use the **one-click script approach** below: generate a `.bat` script with progress output, then elevate it via a VBScript `ShellExecute "runas"` launcher. This requires only one UAC click from the user, after which the entire install runs unattended.

---

## Step 1 — Check environment

```bash
uname -s        # MINGW64 / MSYS / CYGWIN indicates Windows Git Bash
cmd.exe /c ver  # Windows version
```
Check for MySQL client:
```bash
command -v mysql || mysql --version 2>/dev/null
```
If MySQL client is not available, suggest: install via `winget install Oracle.MySQL` or download from <https://dev.mysql.com/downloads/shell/>.

## Step 2 — Download the MSI

```bash
curl -fSL -o /tmp/seekdb.msi "https://mirrors.oceanbase.com/oceanbase/community/stable/windows/11/x86_64/seekdb-1.3.0.0-win64.msi"
```

Check if seekdb is already installed:
```bash
command -v seekdb.exe || where.exe seekdb.exe 2>/dev/null
```
If already installed, skip to Step 5 (verify).

## Step 3 — Generate the one-click install script

Write the following batch script to `%TEMP%\seekdb_setup.bat`. This script runs with Administrator privileges and displays progress in the console window:

```bat
@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul 2>&1
title SeekDB Installer

echo =============================================
echo   SeekDB One-Click Installer for Windows
echo =============================================
echo.

:: Step 1: Install MSI
echo [1/6] Installing SeekDB MSI...
msiexec /i "%TEMP%\seekdb.msi" /qn /norestart WIXUI_EXITDIALOGOPTIONALCHECKBOX=0
if !ERRORLEVEL! NEQ 0 (
    echo       [FAILED] MSI install failed with code !ERRORLEVEL!
    goto :fail
)
echo       [OK] MSI installed successfully.
echo.

:: Step 2: Verify seekdb.exe
echo [2/6] Verifying seekdb.exe...
if not exist "C:\Program Files\seekdb\bin\seekdb.exe" (
    echo       [FAILED] seekdb.exe not found!
    goto :fail
)
echo       [OK] Found: C:\Program Files\seekdb\bin\seekdb.exe
echo.

:: Step 3: Create directories and config
echo [3/6] Creating data directories and config...
mkdir "C:\ProgramData\seekdb\store\redo" 2>nul
mkdir "C:\ProgramData\seekdb\etc" 2>nul
(
echo # seekdb Configuration File
echo base-dir=C:/ProgramData/seekdb
echo data-dir=C:/ProgramData/seekdb/store
echo redo-dir=C:/ProgramData/seekdb/store/redo
echo port=2881
echo cpu_count=4
echo memory_limit=2G
) > "C:\ProgramData\seekdb\etc\seekdb.cnf"
echo       [OK] Config: C:\ProgramData\seekdb\etc\seekdb.cnf
echo.

:: Step 4: Initialize database (background mode)
if exist "C:\ProgramData\seekdb\store\.meta" (
    echo [4/6] Database already initialized, skipping.
    echo.
    goto :install_service
)

echo [4/6] Initializing database (this may take 1-3 minutes)...
echo       Starting seekdb for first-time init...
start "" /B "C:\Program Files\seekdb\bin\seekdb.exe" --base-dir="C:/ProgramData/seekdb" --port=2881 --parameter memory_limit=2G --parameter cpu_count=4

echo       Waiting for database to become ready...
set COUNT=0

:wait_loop
set /a COUNT+=1
if !COUNT! GTR 36 (
    echo       [FAILED] Database not ready after 3 minutes.
    goto :fail
)
timeout /t 5 /nobreak >nul
mysql -h 127.0.0.1 -P 2881 -u root -e "SELECT 1" >nul 2>&1
if !ERRORLEVEL!==0 (
    echo       [OK] Database initialized and ready!
    goto :init_done
)
echo       Waiting... (!COUNT!/36)
goto :wait_loop

:init_done
echo       Stopping init process...
taskkill /F /IM seekdb.exe >nul 2>&1
timeout /t 3 /nobreak >nul
echo.

:: Step 5: Install and start Windows service
:install_service
echo [5/6] Installing Windows service...
"C:\Program Files\seekdb\bin\seekdb.exe" --install-service seekdb --base-dir="C:/ProgramData/seekdb" --port=2881 --parameter memory_limit=2G --parameter cpu_count=4
echo       Service install exit code: !ERRORLEVEL!
sc config seekdb start= auto >nul 2>&1
echo       [OK] Service configured with auto-start.

echo       Starting seekdb service...
sc start seekdb >nul 2>&1
timeout /t 5 /nobreak >nul
echo.

:: Step 6: Verify
echo [6/6] Verifying service and connectivity...
sc query seekdb | findstr "RUNNING" >nul 2>&1
if !ERRORLEVEL!==0 (
    echo       [OK] Service is RUNNING.
) else (
    echo       [WARN] Service may not be running yet.
)

mysql -h 127.0.0.1 -P 2881 -u root -e "SELECT 'SeekDB is running!' AS status;" 2>nul
if !ERRORLEVEL!==0 (
    echo       [OK] MySQL connection successful!
) else (
    echo       [WARN] Cannot connect via MySQL yet. Service may still be starting.
)

echo.
echo =============================================
echo   SeekDB installation completed!
echo =============================================
echo.
echo   Connection:  mysql -h 127.0.0.1 -P 2881 -u root
echo   Config:      C:\ProgramData\seekdb\etc\seekdb.cnf
echo   Data:        C:\ProgramData\seekdb\store
echo.
echo   Service commands:
echo     Start:   sc start seekdb
echo     Stop:    sc stop seekdb
echo     Status:  sc query seekdb
echo.
echo =============================================
echo.
echo Press any key to close...
pause >nul
exit /b 0

:fail
echo.
echo [ERROR] Installation failed. See messages above.
echo Press any key to close...
pause >nul
exit /b 1
```

> **Note on `cpu_count` and `memory_limit`:** Adjust these values in the script based on the user's machine before writing:
> - Development use: `cpu_count=4`, `memory_limit=2G`
> - Server use: `cpu_count` = half of total cores, `memory_limit=4G`
> - Dedicated use: `cpu_count` = total cores, `memory_limit=8G`
>
> Also update the MSI path in the script to match the actual download location (`cygpath -w /tmp/seekdb.msi`).

## Step 4 — Launch the script with UAC elevation

Write a VBScript launcher to elevate the batch script (triggers one UAC prompt, then runs unattended):

```bash
cat > /tmp/seekdb_elevate.vbs << 'VBS'
Set wshShell = CreateObject("WScript.Shell")
Set objShell = CreateObject("Shell.Application")
tempDir = wshShell.ExpandEnvironmentStrings("%TEMP%")
objShell.ShellExecute "cmd.exe", "/c """ & tempDir & "\seekdb_setup.bat""", "", "runas", 1
VBS
```

Launch it:
```bash
cmd.exe //c "wscript.exe $(cygpath -w /tmp/seekdb_elevate.vbs)"
```

Tell the user:
> "A UAC prompt will appear — please click 'Yes'. After that, the installation is fully automatic. The window will show progress for each step and display 'SeekDB installation completed!' when done."

## Step 5 — Verify from the agent side

After the user confirms the installer window has closed, verify:
```bash
mysql -h 127.0.0.1 -P 2881 -u root -e "SELECT 'SeekDB is running!' AS status;"
```

## Step 6 — Done

Confirm success and show connection info:
- MySQL port: `127.0.0.1:2881`
- Config file: `C:\ProgramData\seekdb\etc\seekdb.cnf`
- Data directory: `C:\ProgramData\seekdb\store`
- Service management:
  - Start: `sc.exe start seekdb`
  - Stop: `sc.exe stop seekdb`
  - Status: `sc.exe query seekdb`
  - Restart: `sc.exe stop seekdb && sc.exe start seekdb`
- Uninstall: see the uninstall script below.

---

## Uninstall script

If the user needs to uninstall, generate this batch script and elevate it the same way:

```bat
@echo off
echo ============================================
echo   SeekDB Uninstall
echo ============================================
echo.

echo [1/4] Stopping seekdb service...
sc stop seekdb 2>nul
timeout /t 3 /nobreak >nul
echo       Done.

echo [2/4] Removing seekdb service...
"C:\Program Files\seekdb\bin\seekdb.exe" --remove-service seekdb 2>nul
echo       Done.

echo [3/4] Uninstalling MSI...
msiexec /x "%TEMP%\seekdb.msi" /qn /norestart
echo       MSI uninstall exit code: %ERRORLEVEL%

echo [4/4] Cleaning data directory...
rmdir /s /q "C:\ProgramData\seekdb" 2>nul
echo       Done.

echo.
echo ============================================
echo   SeekDB uninstall completed!
echo ============================================
echo.
echo Press any key to close...
pause >nul
```

---

## Optional — Configure Windows Firewall

If the user needs remote access, add to the install script or run separately:
```bash
netsh advfirewall firewall add rule name="seekdb TCP 2881" dir=in action=allow protocol=TCP localport=2881
```

---

## References

- Windows MSI download: <https://mirrors.oceanbase.com/oceanbase/community/stable/windows/11/x86_64/seekdb-1.3.0.0-win64.msi>
