#Requires -Version 5.1
<#
.SYNOPSIS
    Downloads and installs the VN Tools CLI MSI for the current user.
.DESCRIPTION
    Standalone installer for OpenClaw skill environments. Downloads the MSI from the
    configured URL if not already present in %TEMP%, then runs a silent
    per-user install. Skips if the CLI executable is already installed.
#>

$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12

$MsiVersion  = '0.1.0.0'
$MsiFilename = "vn-tools-cli_${MsiVersion}_windows_x64.msi"
$MsiUrl      = "https://github.com/cawcut/skill-vn/releases/download/0.1.0/${MsiFilename}"
$DownloadConnectTimeoutSeconds = 30
$DownloadMaxTimeSeconds = 3600
$DownloadRetryMaxTimeSeconds = 3600
$PreferredSearchRoot = Join-Path $env:LOCALAPPDATA 'Programs'
$LegacyUserSearchRoot = $env:LOCALAPPDATA
$LegacyMachineSearchRoot = if ($env:ProgramFiles) { $env:ProgramFiles } else { 'C:\Program Files' }
$DownloadDir = Join-Path $env:TEMP 'vn-tools-cli-install'
$MsiPath     = Join-Path $DownloadDir $MsiFilename
$MsiLogPath  = Join-Path $DownloadDir 'vn-tools-cli-install-msi.log'
$CliDisplayName = 'VN Tools CLI'
$CliExecutableName = 'vn-tools-cli.exe'

$CliSearchRoots = @(
    @{ Label = 'per-user-programs';          SearchRoot = $PreferredSearchRoot },
    @{ Label = 'legacy-user-localappdata';   SearchRoot = $LegacyUserSearchRoot },
    @{ Label = 'legacy-machine-programfiles'; SearchRoot = $LegacyMachineSearchRoot }
)

function Test-IsAdministrator {
    try {
        $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
        $principal = [Security.Principal.WindowsPrincipal]::new($identity)
        return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    }
    catch {
        return $false
    }
}

function Find-InstalledCli {
    foreach ($root in $CliSearchRoots) {
        if (-not (Test-Path -LiteralPath $root.SearchRoot)) { continue }

        foreach ($entry in (Get-ChildItem -LiteralPath $root.SearchRoot -Directory -ErrorAction SilentlyContinue)) {
            $candidate = Join-Path $entry.FullName "CLI\bin\$CliExecutableName"
            if (Test-Path -LiteralPath $candidate) {
                return [pscustomobject]@{
                    Label  = $root.Label
                    CliExe = $candidate
                }
            }
        }
    }

    return $null
}

$ExistingInstall = Find-InstalledCli
if ($ExistingInstall) {
    $VersionFilePath = Join-Path (Split-Path $ExistingInstall.CliExe) 'vn-tools-cli.version'
    $InstalledVersion = if (Test-Path -LiteralPath $VersionFilePath) {
        (Get-Content -LiteralPath $VersionFilePath -Raw).Trim()
    } else { $null }

    if ($InstalledVersion -and ([version]$InstalledVersion -ge [version]$MsiVersion)) {
        Write-Host "$CliDisplayName $InstalledVersion is already installed."
        exit 0
    }

    Write-Host "$CliDisplayName $InstalledVersion found -- upgrading to $MsiVersion ..."
}

Write-Host '============================================================'
Write-Host " $CliDisplayName Installer (OpenClaw)"
Write-Host '============================================================'
Write-Host ''
Write-Host "Preferred search root: $PreferredSearchRoot"
Write-Host "Additional search roots: $LegacyUserSearchRoot ; $LegacyMachineSearchRoot"
Write-Host "Running as administrator: $(Test-IsAdministrator)"

if (-not (Test-Path -LiteralPath $DownloadDir)) {
    New-Item -ItemType Directory -Path $DownloadDir -Force | Out-Null
}

if (-not (Test-Path -LiteralPath $MsiPath)) {
    Write-Host "Downloading $MsiFilename ..."
    try {
        $curl = Get-Command 'curl.exe' -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
        if (-not $curl) {
            throw 'curl.exe was not found on PATH.'
        }
        & $curl.Source '--location' '--fail' '--retry' '3' '--retry-all-errors' '--connect-timeout' $DownloadConnectTimeoutSeconds '--max-time' $DownloadMaxTimeSeconds '--retry-max-time' $DownloadRetryMaxTimeSeconds '--progress-bar' '--output' $MsiPath $MsiUrl
        if ($LASTEXITCODE -ne 0) {
            throw "curl.exe failed with exit code $LASTEXITCODE"
        }
        Write-Host ''
    }
    catch {
        Remove-Item -LiteralPath $MsiPath -ErrorAction SilentlyContinue
        Write-Error "Download failed: $_"
        exit 1
    }
    Write-Host "Download complete."
}
else {
    Write-Host "MSI already downloaded: $MsiFilename"
}

Write-Host ''
Write-Host 'Installing MSI (silent) ...'

Remove-Item -LiteralPath $MsiLogPath -ErrorAction SilentlyContinue
& msiexec.exe '/i' $MsiPath 'ALLUSERS=2' 'MSIINSTALLPERUSER=1' '/qn' '/l*v' $MsiLogPath
$MsiExitCode = $LASTEXITCODE
if ($MsiExitCode -ne 0) {
    Write-Host "MSI verbose log: $MsiLogPath"

    if (Test-Path -LiteralPath $MsiLogPath) {
        Write-Host 'Last MSI log lines:'
        Get-Content -LiteralPath $MsiLogPath -Tail 40
    }

    Write-Error "MSI installation failed (exit code: $MsiExitCode)"
    exit 1
}

$InstalledCli = Find-InstalledCli
if (-not $InstalledCli) {
    Write-Error "MSI installation finished, but $CliExecutableName was not found in any search root."
    exit 1
}

$ExeVersion = (Get-Item -LiteralPath $InstalledCli.CliExe).VersionInfo.FileVersion
$VersionFilePath = Join-Path (Split-Path $InstalledCli.CliExe) 'vn-tools-cli.version'
Set-Content -LiteralPath $VersionFilePath -Value $ExeVersion -NoNewline -Encoding ascii

Remove-Item -LiteralPath $MsiPath -ErrorAction SilentlyContinue
Remove-Item -LiteralPath $MsiLogPath -ErrorAction SilentlyContinue

Write-Host ''
Write-Host '============================================================'
Write-Host " Installation complete"
Write-Host " CLI: $($InstalledCli.CliExe)"
Write-Host " Version: $ExeVersion"
Write-Host '============================================================'
exit 0
