# Unihiker K10 Arduino Upload - PowerShell Version
# Usage: .\upload-arduino.ps1 <sketch.ino> [port]

param(
    [Parameter(Mandatory=$true)]
    [string]$Sketch,
    
    [string]$Port = ""
)

$FQBN = "UNIHIKER:esp32:k10"

# Colors
function Write-Info { param($msg) Write-Host "[INFO] $msg" -ForegroundColor Cyan }
function Write-OK { param($msg) Write-Host "[OK] $msg" -ForegroundColor Green }
function Write-Error { param($msg) Write-Host "[ERROR] $msg" -ForegroundColor Red }

# Check sketch file
if (-not (Test-Path $Sketch)) {
    Write-Error "Sketch file not found: $Sketch"
    exit 1
}

$SketchPath = Resolve-Path $Sketch
$SketchDir = Split-Path $SketchPath -Parent
$SketchName = Split-Path $SketchPath -Leaf
$BuildDir = Join-Path $SketchDir "build"

Write-Info "Sketch: $SketchName"
Write-Info "FQBN: $FQBN"
Write-Info "Build dir: $BuildDir"

# Check arduino-cli
$arduinoCli = Get-Command arduino-cli -ErrorAction SilentlyContinue
if (-not $arduinoCli) {
    # Try to find in common locations
    $possiblePaths = @(
        "${env:LOCALAPPDATA}\Arduino15\packages\builtin\tools\arduino-cli\*\arduino-cli.exe",
        "${env:ProgramFiles}\Arduino CLI\arduino-cli.exe",
        "${env:ProgramFiles(x86)}\Arduino CLI\arduino-cli.exe",
        "$PSScriptRoot\arduino-cli.exe",
        "${env:USERPROFILE}\.arduino15\packages\builtin\tools\arduino-cli\*\arduino-cli.exe"
    )
    
    foreach ($path in $possiblePaths) {
        $found = Get-Item $path -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($found) {
            $arduinoCli = $found.FullName
            break
        }
    }
}

if (-not $arduinoCli) {
    Write-Error "arduino-cli not found"
    Write-Host "Please install arduino-cli from https://arduino.github.io/arduino-cli/latest/installation/"
    exit 1
}

Write-Info "Using arduino-cli: $arduinoCli"

# Create build directory
if (-not (Test-Path $BuildDir)) {
    New-Item -ItemType Directory -Path $BuildDir | Out-Null
}

# Detect port if not specified
if ([string]::IsNullOrEmpty($Port)) {
    Write-Info "Detecting K10 port..."
    $ports = & $arduinoCli board list --format json | ConvertFrom-Json
    $k10Port = $ports | Where-Object { $_.matching_boards -and $_.matching_boards.fqbn -like "*unihiker*" } | Select-Object -First 1
    
    if ($k10Port) {
        $Port = $k10Port.port.address
    } else {
        # Try to find any USB serial port
        $usbPort = $ports | Where-Object { $_.port.protocol -eq "serial" -and $_.port.address -like "*USB*" } | Select-Object -First 1
        if ($usbPort) {
            $Port = $usbPort.port.address
        }
    }
}

if ([string]::IsNullOrEmpty($Port)) {
    Write-Error "Could not detect K10 port"
    Write-Host "Please specify port manually or connect K10 board"
    exit 1
}

Write-Info "Port: $Port"

# Compile
Write-Info "Compiling..."
& $arduinoCli compile --fqbn $FQBN --build-path $BuildDir --jobs 0 $SketchPath
if ($LASTEXITCODE -ne 0) {
    Write-Error "Compilation failed"
    exit 1
}
Write-OK "Compilation successful"

# Upload
Write-Info "Uploading to $Port..."
& $arduinoCli upload -p $Port --fqbn $FQBN --input-dir $BuildDir $SketchPath
if ($LASTEXITCODE -ne 0) {
    Write-Error "Upload failed"
    Write-Host "Tips:"
    Write-Host "  - Make sure K10 is in bootloader mode (hold BOOT, press RST)"
    Write-Host "  - Check that the port is correct: $Port"
    exit 1
}

Write-OK "Upload successful!"
Write-Info "Sketch is now running on K10"
