# Detect pyenv, uv, and system Python environments on the M10.
# Usage:
#   .\detect_python_env.ps1
#   .\detect_python_env.ps1 -M10Host 10.1.2.3
#   .\detect_python_env.ps1 -SaveEnvFile ..\.m10-env.json

param(
    [string]$M10Host = "10.1.2.3",
    [string]$User = "root",
    [string]$SaveEnvFile = ""
)

if ($M10Host -notmatch '^[A-Za-z0-9.-]+$' -or $User -notmatch '^[A-Za-z0-9._-]+$') {
    Write-Host "The SSH host or user name contains unsupported characters." -ForegroundColor Red
    exit 1
}

$remoteScript = @'
echo "===M10_PYTHON_ENV_BEGIN==="
echo -n "hostname="
hostname
echo -n "pyenv_global="
(pyenv global 2>/dev/null || cat /root/.python-version 2>/dev/null || echo "")
echo -n "system_python="
(python3 --version 2>/dev/null | awk '{print $2}' || echo "")
echo -n "uv_path="
(command -v uv 2>/dev/null || echo "")
echo -n "uv_version="
(uv --version 2>/dev/null | head -1 || echo "")
echo "pyenv_versions_begin"
(ls -1 /root/.pyenv/versions/ 2>/dev/null || true)
echo "pyenv_versions_end"
for v in $(ls -1 /root/.pyenv/versions/ 2>/dev/null); do
  p="/root/.pyenv/versions/$v/bin/python3"
  if [ -x "$p" ]; then
    echo -n "pyenv_bin_$v="
    echo "$p"
    echo -n "pyenv_ver_$v="
    "$p" --version 2>/dev/null | awk '{print $2}'
  fi
done
echo "===M10_PYTHON_ENV_END==="
'@

Write-Host "=== Detecting M10 Python environments @ ${User}@${M10Host} ===" -ForegroundColor Cyan
Write-Host "SSH may prompt for the factory-default password: dfrobot" -ForegroundColor DarkGray

$raw = ssh -o ConnectTimeout=12 -o StrictHostKeyChecking=accept-new "${User}@${M10Host}" $remoteScript 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "SSH detection failed" -ForegroundColor Red
    Write-Host $raw
    exit 1
}

$env = [ordered]@{
    host         = $M10Host
    hostname     = ""
    pyenv_global = ""
    system_python = ""
    uv_available = $false
    uv_path      = ""
    uv_version   = ""
    pyenv_versions = @()
    python_bins  = @{}
}

$inVersions = $false
foreach ($line in ($raw -split "`n")) {
    $line = $line.Trim()
    if ($line -eq "===M10_PYTHON_ENV_BEGIN===" -or $line -eq "===M10_PYTHON_ENV_END===") { continue }
    if ($line -eq "pyenv_versions_begin") { $inVersions = $true; continue }
    if ($line -eq "pyenv_versions_end") { $inVersions = $false; continue }

    if ($inVersions -and $line) {
        $env.pyenv_versions += $line
        continue
    }
    if ($line -match '^hostname=(.*)$') { $env.hostname = $Matches[1] }
    elseif ($line -match '^pyenv_global=(.*)$') { $env.pyenv_global = $Matches[1] }
    elseif ($line -match '^system_python=(.*)$') { $env.system_python = $Matches[1] }
    elseif ($line -match '^uv_path=(.*)$') { $env.uv_path = $Matches[1]; if ($Matches[1]) { $env.uv_available = $true } }
    elseif ($line -match '^uv_version=(.*)$') { $env.uv_version = $Matches[1] }
    elseif ($line -match '^pyenv_bin_(.+?)=(.*)$') {
        if (-not $env.python_bins.Contains($Matches[1])) { $env.python_bins[$Matches[1]] = @{ bin = $Matches[2] } }
        else { $env.python_bins[$Matches[1]].bin = $Matches[2] }
    }
    elseif ($line -match '^pyenv_ver_(.+?)=(.*)$') {
        if (-not $env.python_bins.Contains($Matches[1])) { $env.python_bins[$Matches[1]] = @{ version = $Matches[2] } }
        else { $env.python_bins[$Matches[1]].version = $Matches[2] }
    }
}

Write-Host ""
Write-Host "Host: $($env.hostname) @ $($env.host)" -ForegroundColor Green
Write-Host "System python3: $($env.system_python)"
Write-Host "Global pyenv version: $($env.pyenv_global)"
if ($env.pyenv_versions.Count -gt 0) {
    Write-Host "Installed pyenv versions:"
    foreach ($v in $env.pyenv_versions) {
        $bin = $env.python_bins[$v].bin
        Write-Host "  - $v  =>  $bin"
    }
} else {
    Write-Host "pyenv versions: none found under /root/.pyenv/versions/"
}
if ($env.uv_available) {
    Write-Host "uv: $($env.uv_path)  $($env.uv_version)" -ForegroundColor Green
} else {
    Write-Host "uv: not installed (images older than V0.4.5 may not include it)"
}

# Recommended default
$recommended = $env.pyenv_global
if (-not $recommended -and $env.pyenv_versions.Count -gt 0) {
    $recommended = $env.pyenv_versions[-1]
}
if ($recommended) {
    Write-Host ""
    Write-Host "Recommended default: pyenv $recommended (official V0.4.5+ images default to 3.12.7)" -ForegroundColor Cyan
}

if ($SaveEnvFile) {
    $defaultBin = if ($recommended -and $env.python_bins.Contains($recommended)) {
        $env.python_bins[$recommended].bin
    } else { "python3" }
    $out = @{
        host            = $M10Host
        mode            = "pyenv"
        python_version  = $recommended
        python_bin      = $defaultBin
        uv_path         = $env.uv_path
        uv_available    = $env.uv_available
        detected_at     = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    } | ConvertTo-Json -Depth 4
    $dir = Split-Path $SaveEnvFile -Parent
    if ($dir -and -not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
    $out | Set-Content -Path $SaveEnvFile -Encoding UTF8
    Write-Host "Saved environment configuration: $SaveEnvFile" -ForegroundColor Green
}

Write-Host ""
Write-Host "Next: ask the user to select a detected pyenv version, uv, or system Python." -ForegroundColor Yellow
exit 0
