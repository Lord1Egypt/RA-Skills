# setup.ps1 - prepare this machine for the Windows Multi-Tool Suite.
#
# Reviewable PowerShell. It does not install an unknown binary, it does not
# ask for admin rights, and it does not touch anything outside your user
# profile. Run it again any time: it is idempotent.
#
# Usage (PowerShell 5.1+ on Windows 10/11):
#   Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
#   Unblock-File .\scripts\setup.ps1
#   .\scripts\setup.ps1
#
# Options:
#   -Workspace <path>   Where to keep config, output, and shortcuts
#   -SkipSkillInstall   Do not touch the ClawHub CLI (offline setup)
#   -WhatIf             Print the plan and change nothing

[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string]$Workspace = "",
    [switch]$SkipSkillInstall,
    [switch]$WhatIf
)

$ErrorActionPreference = "Stop"

$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$BundleRoot = Split-Path -Parent $ScriptRoot
$ExampleConfig = Join-Path $BundleRoot "config.example.json"

function Write-Step($message) { Write-Host "==> $message" -ForegroundColor Cyan }
function Write-Ok($message) { Write-Host "    ok: $message" -ForegroundColor Green }
function Write-Warn2($message) { Write-Host "    warn: $message" -ForegroundColor Yellow }
function Write-Err2($message) { Write-Host "    error: $message" -ForegroundColor Red }

Write-Host ""
Write-Host "Windows Multi-Tool Suite - setup" -ForegroundColor White
Write-Host "-----------------------------------"

# --- 1. Machine check -------------------------------------------------------
Write-Step "Checking this machine"

if (-not $IsWindows -and $PSVersionTable.PSVersion.Major -lt 6) {
    Write-Err2 "This setup targets Windows 10/11 with PowerShell 5.1 or later."
    exit 2
}
$os = Get-CimInstance Win32_OperatingSystem
Write-Ok "$($os.Caption) build $($os.BuildNumber)"

if (-not [Environment]::Is64BitOperatingSystem) {
    Write-Err2 "This kit is 64-bit only (Windows 10/11, 64-bit)."
    exit 2
}
Write-Ok "64-bit operating system"

$psVersion = $PSVersionTable.PSVersion.ToString()
if ([version]$psVersion -lt [version]"5.1") {
    Write-Err2 "PowerShell 5.1 or later is required (found $psVersion)."
    exit 2
}
Write-Ok "PowerShell $psVersion"

$python = $null
foreach ($candidate in @("python", "python3", "py")) {
    $found = Get-Command $candidate -ErrorAction SilentlyContinue
    if ($found) { $python = $found.Source; break }
}
if ($python) {
    $pyVersion = (& $python --version 2>&1) -join " "
    Write-Ok "Python: $python ($pyVersion)"
    if ($pyVersion -match "(\d+)\.(\d+)") {
        if ([int]$Matches[1] -lt 3 -or ([int]$Matches[1] -eq 3 -and [int]$Matches[2] -lt 9)) {
            Write-Warn2 "Python 3.9 or later is recommended for the workflow scripts."
        }
    }
} else {
    Write-Warn2 "Python was not found. The workflow scripts need Python 3.9+."
}

$clawhub = Get-Command "clawhub" -ErrorAction SilentlyContinue
if ($clawhub) {
    Write-Ok "ClawHub CLI: $($clawhub.Source)"
} elseif (-not $SkipSkillInstall) {
    Write-Warn2 "ClawHub CLI was not found. Install it with 'npm i -g clawhub' to pull the skills automatically."
}

# --- 2. Workspace ----------------------------------------------------------
if (-not $Workspace) {
    $Workspace = Join-Path $env:LOCALAPPDATA "MultiToolSuite"
}
Write-Step "Preparing the workspace at $Workspace"

if ($PSCmdlet.ShouldProcess($Workspace, "Create or update the MultiToolSuite workspace")) {
    foreach ($sub in @("", "output", "output\creative", "output\market", "output\leads")) {
        $path = if ($sub) { Join-Path $Workspace $sub } else { $Workspace }
        if (-not (Test-Path $path)) { New-Item -ItemType Directory -Path $path -Force | Out-Null }
    }
    Write-Ok "workspace folders ready"

    $configPath = Join-Path $Workspace "config.json"
    if (Test-Path $configPath) {
        Write-Ok "config.json already exists - left untouched"
    } elseif (Test-Path $ExampleConfig) {
        Copy-Item $ExampleConfig $configPath -Force
        Write-Ok "config.json written from config.example.json (no keys in it - add your own)"
    } else {
        Write-Warn2 "config.example.json not found next to this script; no config written."
    }
} else {
    Write-Warn2 "skipped (WhatIf)"
}

# --- 3. Skills -------------------------------------------------------------
if (-not $SkipSkillInstall) {
    Write-Step "Installing the catalog skills"
    $skills = @(
        "ai-creative-studio",
        "ai-trading",
        "b2b-lead-research-agent"
    )
    $installCmd = Get-Command "clawhub" -ErrorAction SilentlyContinue
    if (-not $installCmd) {
        Write-Warn2 "ClawHub CLI not available. Install the skills manually:"
        foreach ($s in $skills) { Write-Host "        clawhub install @rapidworker1/$s" }
    } else {
        foreach ($s in $skills) {
            if ($PSCmdlet.ShouldProcess("skill:$s", "Install @rapidworker1/$s")) {
                & $installCmd.Source install "@rapidworker1/$s" --no-input 2>&1 | ForEach-Object { Write-Host "        $_" }
                if ($LASTEXITCODE -eq 0) { Write-Ok "installed $s" } else { Write-Warn2 "could not install $s - install it later with 'clawhub install @rapidworker1/$s'" }
            }
        }
    }
} else {
    Write-Step "Skipping skill installation (as requested)"
}

# --- 4. Launcher shortcut --------------------------------------------------
Write-Step "Adding the launcher shortcut"
$startMenu = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs"
$shortcutPath = Join-Path $startMenu "Multi-Tool Suite.lnk"
$launcher = Join-Path $ScriptRoot "MultiTool.ps1"
if ($PSCmdlet.ShouldProcess($shortcutPath, "Create the Start Menu shortcut")) {
    try {
        if (-not (Test-Path $startMenu)) { New-Item -ItemType Directory -Path $startMenu -Force | Out-Null }
        $shell = New-Object -ComObject WScript.Shell
        $shortcut = $shell.CreateShortcut($shortcutPath)
        $shortcut.TargetPath = "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe"
        $shortcut.Arguments = "-NoProfile -ExecutionPolicy RemoteSigned -File `"$launcher`""
        $shortcut.WorkingDirectory = $Workspace
        $shortcut.IconLocation = "$env:SystemRoot\System32\shell32.dll,21"
        $shortcut.Save()
        Write-Ok "Start Menu shortcut created"
    } catch {
        Write-Warn2 "Could not create the shortcut: $($_.Exception.Message). Run scripts\MultiTool.ps1 directly."
    }
} else {
    Write-Warn2 "skipped (WhatIf)"
}

# --- 5. Verify -------------------------------------------------------------
Write-Step "Verifying the install"
$verify = Join-Path $ScriptRoot "verify_install.py"
if ($python -and (Test-Path $verify)) {
    & $python $verify
    if ($LASTEXITCODE -eq 0) { Write-Ok "install verified" } else { Write-Warn2 "verification reported items to fix (see above)" }
} else {
    Write-Warn2 "Run 'python scripts\verify_install.py' after Python is available."
}

Write-Host ""
Write-Host "Done." -ForegroundColor Green
Write-Host "Launcher : $launcher"
Write-Host "Workspace: $Workspace"
Write-Host "Next     : read references\faq.md for the questions buyers ask."
Write-Host ""
