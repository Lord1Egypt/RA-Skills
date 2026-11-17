# Upload a .py file to the M10 and run it in the selected Python or uv environment.
# Usage:
#   .\run_on_m10.ps1 .\hello.py
#   .\run_on_m10.ps1 .\hello.py -Background
#   .\run_on_m10.ps1 .\hello.py -EnvFile ..\.m10-env.json
#   .\run_on_m10.ps1 .\hello.py -Mode uv -PythonBin /root/.pyenv/versions/3.12.7/bin/python3
#   .\run_on_m10.ps1 .\hello.py -PipInstall requests -OfflinePipInstall

param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Script,
    [string]$M10Host = "10.1.2.3",
    [string]$User = "root",
    [string]$EnvFile = "",
    [ValidateSet("pyenv", "uv", "system", "")]
    [string]$Mode = "",
    [string]$PythonBin = "",
    [string]$UvPath = "uv",
    [switch]$Background,
    [string]$PipInstall = "",
    [switch]$OfflinePipInstall
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $Script)) {
    Write-Error "File does not exist: $Script"
    exit 1
}

# Read .m10-env.json
if ($EnvFile -and (Test-Path $EnvFile)) {
    $cfg = Get-Content $EnvFile -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($cfg.host) { $M10Host = $cfg.host }
    if ($cfg.mode -and -not $Mode) { $Mode = $cfg.mode }
    if ($cfg.python_bin -and -not $PythonBin) { $PythonBin = $cfg.python_bin }
    if ($cfg.uv_path) { $UvPath = $cfg.uv_path }
}

if ($M10Host -notmatch '^[A-Za-z0-9.-]+$' -or $User -notmatch '^[A-Za-z0-9._-]+$') {
    Write-Error "The SSH host or user name contains unsupported characters."
    exit 1
}

if (-not $Mode) { $Mode = if ($PythonBin) { "pyenv" } else { "system" } }
if (-not $PythonBin -and $Mode -eq "system") { $PythonBin = "python3" }
if (-not $PythonBin -and $Mode -eq "pyenv") {
    $PythonBin = "/root/.pyenv/versions/3.12.7/bin/python3"
}

if ($PythonBin -and $PythonBin -notmatch '^[/A-Za-z0-9._-]+$') {
    Write-Error "PythonBin contains unsupported characters."
    exit 1
}
if ($UvPath -notmatch '^[/A-Za-z0-9._-]+$') {
    Write-Error "UvPath contains unsupported characters."
    exit 1
}
if ($PipInstall -and $PipInstall -notmatch '^[A-Za-z0-9_.\-\[\],<>=!~ ]+$') {
    Write-Error "PipInstall must contain only package names and version specifiers."
    exit 1
}

function Get-RunCommand([string]$remotePath, [string]$logPath) {
    switch ($Mode) {
        "uv" {
            if ($Background) {
                return "pkill -f $remotePath 2>/dev/null; nohup $UvPath run python $remotePath > $logPath 2>&1 & sleep 2; head -5 $logPath"
            }
            return "$UvPath run python $remotePath"
        }
        default {
            if ($Background) {
                return "pkill -f $remotePath 2>/dev/null; nohup $PythonBin $remotePath > $logPath 2>&1 & sleep 2; head -5 $logPath"
            }
            return "$PythonBin $remotePath"
        }
    }
}

function Get-PipCommand([string]$package) {
    switch ($Mode) {
        "uv" { return "$UvPath pip install $package" }
        default { return "$PythonBin -m pip install $package" }
    }
}

$localFile = (Resolve-Path $Script).Path
$fileName = [regex]::Replace((Split-Path $localFile -Leaf), '[^A-Za-z0-9._-]', '_')
$remoteDir = "/tmp/m10_nl"
$remotePath = "$remoteDir/$fileName"
$logPath = "/tmp/${fileName}.log"

Write-Host "=== Deploying to UNIHIKER M10 ===" -ForegroundColor Cyan
Write-Host "Local: $localFile"
Write-Host "Remote: ${User}@${M10Host}:$remotePath"
Write-Host "Environment: mode=$Mode  python=$PythonBin" $(if ($Mode -eq "uv") { "uv=$UvPath" })
Write-Host "SSH/SCP may prompt for the factory-default password: dfrobot"
Write-Host ""

ssh -o StrictHostKeyChecking=accept-new "${User}@${M10Host}" "mkdir -p $remoteDir"
scp -o StrictHostKeyChecking=accept-new $localFile "${User}@${M10Host}:${remotePath}"

if ($PipInstall) {
    Write-Host "Installing dependency: $PipInstall"
    if ($OfflinePipInstall) {
        $offlineInstaller = Join-Path $PSScriptRoot "install_m10_package_offline.ps1"
        $offlineArgs = @(
            "-ExecutionPolicy", "Bypass", "-File", $offlineInstaller,
            $PipInstall, "-M10Host", $M10Host, "-User", $User,
            "-Mode", $Mode, "-PythonBin", $PythonBin, "-UvPath", $UvPath
        )
        powershell @offlineArgs
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Offline dependency installation failed."
            exit $LASTEXITCODE
        }
    } else {
        $pipCmd = Get-PipCommand $PipInstall
        ssh -o StrictHostKeyChecking=accept-new "${User}@${M10Host}" $pipCmd
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Dependency installation failed. Use -OfflinePipInstall when the M10 has no Internet access."
            exit $LASTEXITCODE
        }
    }
}

$runCmd = Get-RunCommand $remotePath $logPath
if ($Background) {
    Write-Host "Starting in the background..."
} else {
    Write-Host "Running in the foreground..."
}
ssh -o StrictHostKeyChecking=accept-new "${User}@${M10Host}" $runCmd

if ($LASTEXITCODE -eq 0) {
    Write-Host "Completed" -ForegroundColor Green
} else {
    Write-Host "Exit code: $LASTEXITCODE" -ForegroundColor Yellow
}
