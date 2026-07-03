param(
    [Parameter(Mandatory = $true)]
    [string]$OutFile,

    [string]$CoreDir = $(if ($env:PLATFORMIO_CORE_DIR) { $env:PLATFORMIO_CORE_DIR } else { Join-Path $env:USERPROFILE ".platformio" }),

    [string]$PioBin = "pio"
)

$ErrorActionPreference = "Stop"

$outExt = [System.IO.Path]::GetExtension($OutFile).ToLowerInvariant()
if (($outExt -ne ".exe") -and ($outExt -ne ".zip")) {
    Write-Error "Output file must end with .exe or .zip"
    exit 1
}
$makeExe = $outExt -eq ".exe"

if ($makeExe) {
    $iexpress = Join-Path $env:SystemRoot "System32\iexpress.exe"
    if (-not (Test-Path $iexpress)) {
        Write-Error "iexpress.exe not found. Cannot create a self-extracting .exe on this Windows machine."
        exit 1
    }
}

if (-not (Test-Path $CoreDir)) {
    Write-Error "PlatformIO core directory not found: $CoreDir"
    exit 1
}

$required = @(
    "platforms\unihiker",
    "packages\framework-arduinounihiker",
    "packages\toolchain-riscv32-esp",
    "packages\toolchain-xtensa-esp32",
    "packages\toolchain-xtensa-esp32s3",
    "packages\tool-esptoolpy",
    "packages\tool-scons",
    "packages\tool-mkfatfs",
    "packages\tool-mklittlefs",
    "packages\tool-mkspiffs"
)

$missing = @()
foreach ($path in $required) {
    if (-not (Test-Path (Join-Path $CoreDir $path))) {
        $missing += $path
    }
}

if ($missing.Count -gt 0) {
    Write-Error ("Missing PlatformIO support files in {0}:`n  - {1}`nBuild a K10 PlatformIO project once on this Windows machine, then rerun this script." -f $CoreDir, ($missing -join "`n  - "))
    exit 1
}

$pythonRoot = Join-Path $CoreDir "python3"
$pythonExe = Join-Path $pythonRoot "python.exe"
$sitePackages = Join-Path $CoreDir "penv\Lib\site-packages"

if (-not (Test-Path $pythonExe)) {
    Write-Error "Bundled PlatformIO Python not found: $pythonExe"
    Write-Error "Install PlatformIO Core with the official Windows installer or use a prepared self-contained PlatformIO core directory."
    exit 1
}

if (-not (Test-Path (Join-Path $sitePackages "platformio"))) {
    Write-Error "PlatformIO Python package not found in: $sitePackages"
    Write-Error "Run '$PioBin --version' and build a K10 PlatformIO project once, then rerun this script."
    exit 1
}

$arch = if ([Environment]::Is64BitOperatingSystem) { "x64" } else { "x86" }
if ($arch -ne "x64") {
    Write-Error "This installer supports 64-bit Windows only. Current OS architecture: $arch"
    exit 1
}

$pkgName = "K10P-windows-x64"
$rootName = "K10P"
$stage = Join-Path ([System.IO.Path]::GetTempPath()) ("k10p-win-" + [System.Guid]::NewGuid().ToString("N"))
$root = Join-Path $stage $rootName

function Copy-Tree {
    param(
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][string]$Destination
    )

    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $Destination) | Out-Null
    Copy-Item -LiteralPath $Source -Destination $Destination -Recurse -Force
}

function Write-Text {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Text
    )

    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $Path) | Out-Null
    [System.IO.File]::WriteAllText($Path, $Text, [System.Text.Encoding]::ASCII)
}

try {
    New-Item -ItemType Directory -Force -Path (Join-Path $root ".platformio") | Out-Null
    New-Item -ItemType Directory -Force -Path (Join-Path $root "examples\Blink\src") | Out-Null

    foreach ($path in $required) {
        Copy-Tree -Source (Join-Path $CoreDir $path) -Destination (Join-Path (Join-Path $root ".platformio") $path)
    }

    Copy-Tree -Source $pythonRoot -Destination (Join-Path (Join-Path $root ".platformio") "python3")
    Copy-Tree -Source $sitePackages -Destination (Join-Path (Join-Path $root ".platformio") "penv\Lib\site-packages")

    Write-Text -Path (Join-Path $root "examples\Blink\platformio.ini") -Text @'
[env:unihiker]
platform = https://github.com/DFRobot/platform-unihiker.git
board = unihiker_k10
framework = arduino
build_flags =
    -DARDUINO_USB_CDC_ON_BOOT=1
    -DARDUINO_USB_MODE=1
    -DModel=None
monitor_speed = 115200
'@

    Write-Text -Path (Join-Path $root "examples\Blink\src\main.cpp") -Text @'
#include <Arduino.h>
#include "unihiker_k10.h"

UNIHIKER_K10 k10;

void setup() {
  Serial.begin(115200);
  k10.begin();
  k10.initScreen(2);
  k10.creatCanvas();
  k10.setScreenBackground(0xFFFFFF);
  k10.canvas->canvasText("UNIHIKER", 1, 0x0000FF);
  k10.canvas->updateCanvas();
}

void loop() {
  delay(1000);
}
'@

    Write-Text -Path (Join-Path $root "setup-platformio.bat") -Text @'
@echo off
setlocal
set "ROOT=%~dp0"
set "ROOT=%ROOT:~0,-1%"
set "PLATFORMIO_CORE_DIR=%ROOT%\.platformio"
set "PYTHONPATH=%ROOT%\.platformio\penv\Lib\site-packages"
echo [INFO] K10P root: %ROOT%
"%ROOT%\.platformio\python3\python.exe" -m platformio --version
if errorlevel 1 exit /b %errorlevel%
echo [OK] K10 PlatformIO is ready.
echo [INFO] Test build:
echo   "%ROOT%\pio.bat" run -d "%ROOT%\examples\Blink"
'@

    Write-Text -Path (Join-Path $root "pio.bat") -Text @'
@echo off
setlocal
set "ROOT=%~dp0"
set "ROOT=%ROOT:~0,-1%"
set "PLATFORMIO_CORE_DIR=%ROOT%\.platformio"
set "PYTHONPATH=%ROOT%\.platformio\penv\Lib\site-packages"
"%ROOT%\.platformio\python3\python.exe" -m platformio %*
'@

    Write-Text -Path (Join-Path $root "platformio.bat") -Text @'
@echo off
call "%~dp0pio.bat" %*
'@

    Write-Text -Path (Join-Path $root "compile-project.bat") -Text @'
@echo off
if "%~1"=="" (
  echo Usage: %~nx0 ^<PlatformIOProject^>
  exit /b 1
)
call "%~dp0pio.bat" run -d "%~1"
'@

    Write-Text -Path (Join-Path $root "upload-project.bat") -Text @'
@echo off
if "%~1"=="" (
  echo Usage: %~nx0 ^<PlatformIOProject^> [COM-port]
  exit /b 1
)
if "%~2"=="" (
  call "%~dp0pio.bat" run -d "%~1" -t upload
) else (
  call "%~dp0pio.bat" run -d "%~1" -t upload --upload-port "%~2"
)
'@

    Write-Text -Path (Join-Path $root "monitor-project.bat") -Text @'
@echo off
if "%~1"=="" (
  echo Usage: %~nx0 ^<PlatformIOProject^> [COM-port]
  exit /b 1
)
if "%~2"=="" (
  call "%~dp0pio.bat" device monitor -d "%~1"
) else (
  call "%~dp0pio.bat" device monitor -d "%~1" --port "%~2"
)
'@

    Write-Text -Path (Join-Path $root "README-Windows.txt") -Text @"
K10 PlatformIO Windows offline installer
========================================

Prepared for: Windows x64

1. Copy this $rootName folder from the USB drive to a short path, for example:
   C:\K10P

2. Open Command Prompt or PowerShell and run:
   cd C:\K10P
   setup-platformio.bat

3. Verify:
   pio.bat --version
   pio.bat run -d examples\Blink

4. Build or upload a student project:
   compile-project.bat "C:\path\to\PlatformIOProject"
   upload-project.bat "C:\path\to\PlatformIOProject" COM3
   monitor-project.bat "C:\path\to\PlatformIOProject" COM3

Notes:
- Keep this folder and projects in short paths such as C:\K10P and C:\K10Work.
- The scripts use this folder's private .platformio directory.
- Use pio.bat or platformio.bat from this folder instead of any system pio command.
"@

    $pioVersion = try { & $PioBin --version 2>$null } catch { "unknown" }
    $pythonVersion = & $pythonExe --version 2>&1
    Write-Text -Path (Join-Path $root "metadata.txt") -Text @"
name=$pkgName
created_at=$((Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ"))
windows_arch=x64
platformio_core_dir=$CoreDir
platformio_version=$pioVersion
python=$pythonVersion
"@

    $outParent = Split-Path -Parent $OutFile
    if ([string]::IsNullOrWhiteSpace($outParent)) {
        $outParent = "."
    }
    New-Item -ItemType Directory -Force -Path $outParent | Out-Null
    $outParentPath = (Resolve-Path -LiteralPath $outParent).Path
    $outFilePath = Join-Path $outParentPath (Split-Path -Leaf $OutFile)
    if (Test-Path $outFilePath) {
        Remove-Item -LiteralPath $outFilePath -Force
    }

    if ($makeExe) {
        $sfxDir = Join-Path $stage "sfx"
        New-Item -ItemType Directory -Force -Path $sfxDir | Out-Null
        $payloadZip = Join-Path $sfxDir "K10P-payload.zip"
        $installCmd = Join-Path $sfxDir "install.cmd"
        $sedFile = Join-Path $stage "K10P-windows-x64.sed"

        Compress-Archive -Path $root -DestinationPath $payloadZip -CompressionLevel Optimal

        Write-Text -Path $installCmd -Text @'
@echo off
setlocal
set "TARGET=C:\K10P"
echo K10 PlatformIO Windows offline installer
echo Target: %TARGET%
echo.
if exist "%TARGET%" (
  echo Existing %TARGET% will be replaced.
  set /p ANSWER=Continue? [Y/N] 
  if /I not "%ANSWER%"=="Y" exit /b 1
  rmdir /s /q "%TARGET%"
)
powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -LiteralPath '%~dp0K10P-payload.zip' -DestinationPath 'C:\' -Force"
if errorlevel 1 exit /b %errorlevel%
call "%TARGET%\setup-platformio.bat"
echo.
echo Installed to %TARGET%.
pause
'@

        $sed = @"
[Version]
Class=IEXPRESS
SEDVersion=3
[Options]
PackagePurpose=InstallApp
ShowInstallProgramWindow=1
HideExtractAnimation=0
UseLongFileName=1
InsideCompressed=0
CAB_FixedSize=0
CAB_ResvCodeSigning=0
RebootMode=N
InstallPrompt=This will install K10 PlatformIO to C:\K10P.
DisplayLicense=
FinishMessage=K10 PlatformIO installer finished.
TargetName=$outFilePath
FriendlyName=K10 PlatformIO Windows Offline Installer
AppLaunched=install.cmd
PostInstallCmd=<None>
AdminQuietInstCmd=
UserQuietInstCmd=
SourceFiles=SourceFiles
[SourceFiles]
SourceFiles0=$sfxDir\
[SourceFiles0]
%FILE0%=
%FILE1%=
[Strings]
FILE0="K10P-payload.zip"
FILE1="install.cmd"
"@
        Write-Text -Path $sedFile -Text $sed
        & $iexpress /N $sedFile
        if ($LASTEXITCODE -ne 0) {
            Write-Error "iexpress.exe failed with exit code $LASTEXITCODE"
            exit $LASTEXITCODE
        }

        $deadline = (Get-Date).AddSeconds(120)
        while ((-not (Test-Path $outFilePath)) -and ((Get-Date) -lt $deadline)) {
            Start-Sleep -Milliseconds 500
        }
        if (-not (Test-Path $outFilePath)) {
            Write-Error "iexpress.exe completed but did not create: $outFilePath"
            exit 1
        }

        $sizeMb = [math]::Round((Get-Item $outFilePath).Length / 1MB, 1)
        Write-Host "[OK] Windows self-extracting installer written: $outFilePath"
        Write-Host "[INFO] Installer size: $sizeMb MB"
        Write-Host "[INFO] Copy this .exe to a USB drive, then run it on Windows x64 machines. It installs to C:\K10P."
    } else {
        Compress-Archive -Path $root -DestinationPath $outFilePath -CompressionLevel Optimal

        $sizeMb = [math]::Round((Get-Item $outFilePath).Length / 1MB, 1)
        Write-Host "[OK] Windows offline archive written: $outFilePath"
        Write-Host "[INFO] Archive size: $sizeMb MB"
        Write-Host "[INFO] Copy this .zip to a USB drive, extract it on Windows x64 machines, then run C:\K10P\setup-platformio.bat."
    }
}
finally {
    if (Test-Path $stage) {
        Remove-Item -LiteralPath $stage -Recurse -Force
    }
}


