# Download ARM64 Python wheels on the computer, upload them, and install them on an offline M10.
# Usage:
#   .\install_m10_package_offline.ps1 requests -EnvFile ..\.m10-env.json
#   .\install_m10_package_offline.ps1 "requests==2.32.4" -M10Host 10.1.2.3

param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Package,
    [string]$M10Host = "10.1.2.3",
    [string]$User = "root",
    [string]$EnvFile = "",
    [ValidateSet("pyenv", "uv", "system", "")]
    [string]$Mode = "",
    [string]$PythonBin = "",
    [string]$UvPath = "uv",
    [string]$Wheelhouse = ""
)

$ErrorActionPreference = "Stop"

if ($EnvFile -and (Test-Path -LiteralPath $EnvFile)) {
    $cfg = Get-Content -LiteralPath $EnvFile -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($cfg.host) { $M10Host = $cfg.host }
    if ($cfg.mode -and -not $Mode) { $Mode = $cfg.mode }
    if ($cfg.python_bin -and -not $PythonBin) { $PythonBin = $cfg.python_bin }
    if ($cfg.uv_path) { $UvPath = $cfg.uv_path }
}

if ($M10Host -notmatch '^[A-Za-z0-9.-]+$' -or $User -notmatch '^[A-Za-z0-9._-]+$') {
    Write-Error "The SSH host or user name contains unsupported characters."
    exit 1
}
if ($Package -notmatch '^[A-Za-z0-9_.\-\[\],<>=!~]+$') {
    Write-Error "Package must be one PyPI package name with optional extras or a version specifier."
    exit 1
}

if (-not $Mode) { $Mode = if ($PythonBin) { "pyenv" } else { "system" } }
if (-not $PythonBin -and $Mode -eq "system") { $PythonBin = "python3" }
if (-not $PythonBin -and $Mode -eq "pyenv") {
    $PythonBin = "/root/.pyenv/versions/3.12.7/bin/python3"
}
if (-not $PythonBin -and $Mode -eq "uv") {
    Write-Error "The uv mode needs python_bin in the environment file so wheels match the selected interpreter."
    exit 1
}
if ($PythonBin -notmatch '^[/A-Za-z0-9._-]+$' -or $UvPath -notmatch '^[/A-Za-z0-9._-]+$') {
    Write-Error "PythonBin or UvPath contains unsupported characters."
    exit 1
}

function Find-LocalPip {
    $candidates = @(
        [pscustomobject]@{ File = "py"; Prefix = @("-3") },
        [pscustomobject]@{ File = "python"; Prefix = @() },
        [pscustomobject]@{ File = "python3"; Prefix = @() }
    )

    foreach ($candidate in $candidates) {
        if (-not (Get-Command $candidate.File -ErrorAction SilentlyContinue)) { continue }
        & $candidate.File @($candidate.Prefix) -m pip --version *> $null
        if ($LASTEXITCODE -eq 0) { return $candidate }
    }
    return $null
}

$localPip = Find-LocalPip
if (-not $localPip) {
    Write-Error "Offline dependency installation needs Python and pip on the computer. Install Python 3 with pip, then retry."
    exit 1
}

$deleteLocalWheelhouse = $false
if ($Wheelhouse) {
    $localWheelhouse = [IO.Path]::GetFullPath($Wheelhouse)
    New-Item -ItemType Directory -Path $localWheelhouse -Force | Out-Null
} else {
    $localWheelhouse = Join-Path ([IO.Path]::GetTempPath()) ("unihiker-m10-wheels-" + [guid]::NewGuid().ToString("N"))
    New-Item -ItemType Directory -Path $localWheelhouse | Out-Null
    $deleteLocalWheelhouse = $true
}

try {
    $uploadId = "pkg-" + [guid]::NewGuid().ToString("N")
    $remoteParent = "/tmp/m10_nl/wheelhouse"
    $remoteWheelhouse = "$remoteParent/$uploadId"
    $probeCode = 'import platform,sys; print("%d.%d" % sys.version_info[:2]); print(platform.machine()); print(platform.libc_ver()[1])'
    $probeCommand = "$PythonBin -c '$probeCode'; mkdir -p '$remoteParent'"

    Write-Host "=== Preparing an offline M10 dependency ===" -ForegroundColor Cyan
    Write-Host "Package: $Package"
    Write-Host "Target: ${User}@${M10Host}  mode=$Mode  python=$PythonBin"
    Write-Host "SSH/SCP may prompt for the factory-default password: dfrobot"

    $probe = @(ssh -o ConnectTimeout=12 -o StrictHostKeyChecking=accept-new "${User}@${M10Host}" $probeCommand)
    if ($LASTEXITCODE -ne 0 -or $probe.Count -lt 2) {
        Write-Error "Could not inspect the selected Python environment on the M10."
        exit 1
    }

    $pythonVersion = $probe[0].Trim()
    $machine = $probe[1].Trim().ToLowerInvariant()
    $glibcVersion = if ($probe.Count -ge 3) { $probe[2].Trim() } else { "" }
    if ($pythonVersion -notmatch '^(\d+)\.(\d+)$') {
        Write-Error "Unexpected target Python version: $pythonVersion"
        exit 1
    }
    $pythonMajor = [int]$Matches[1]
    $pythonMinor = [int]$Matches[2]
    if ($machine -notin @("aarch64", "arm64")) {
        Write-Error "Expected the M10 ARM64 architecture, but the selected environment reported: $machine"
        exit 1
    }

    $pythonTag = "$pythonMajor$pythonMinor"
    $abis = @("cp$pythonTag", "abi3", "none")
    if ($pythonMajor -eq 3 -and $pythonMinor -le 7) { $abis[0] = "cp${pythonTag}m" }

    $platforms = [Collections.Generic.List[string]]::new()
    if ($glibcVersion -match '^2\.(\d+)$') {
        $glibcMinor = [int]$Matches[1]
        for ($minor = $glibcMinor; $minor -ge 17; $minor--) {
            $platforms.Add("manylinux_2_${minor}_aarch64")
        }
    }
    if (-not $platforms.Contains("manylinux_2_17_aarch64")) {
        $platforms.Add("manylinux_2_17_aarch64")
    }
    $platforms.Add("manylinux2014_aarch64")

    $downloadArgs = @($localPip.Prefix) + @(
        "-m", "pip", "download", $Package,
        "--dest", $localWheelhouse,
        "--only-binary=:all:",
        "--implementation", "cp",
        "--python-version", $pythonTag,
        "--no-cache-dir"
    )
    foreach ($platform in $platforms) { $downloadArgs += @("--platform", $platform) }
    foreach ($abi in $abis) { $downloadArgs += @("--abi", $abi) }

    Write-Host "Downloading wheels for CPython $pythonVersion / aarch64..."
    & $localPip.File @downloadArgs
    if ($LASTEXITCODE -ne 0) {
        Write-Error "No complete compatible wheel set was found. Pin another package version or build the dependency on an ARM64 Linux system."
        exit 2
    }

    $wheels = @(Get-ChildItem -LiteralPath $localWheelhouse -Filter *.whl -File)
    if ($wheels.Count -eq 0) {
        Write-Error "pip completed without producing any wheel files."
        exit 2
    }

    Write-Host "Uploading $($wheels.Count) wheel file(s)..."
    scp -o StrictHostKeyChecking=accept-new -r $localWheelhouse "${User}@${M10Host}:${remoteWheelhouse}"
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Wheel upload failed."
        exit 1
    }

    if ($Mode -eq "uv") {
        $installCommand = "$UvPath pip install --python $PythonBin --no-index --find-links '$remoteWheelhouse' '$Package'"
    } else {
        $installCommand = "$PythonBin -m pip install --no-index --find-links '$remoteWheelhouse' '$Package'"
    }
    $installAndClean = "$installCommand; status=`$?; rm -rf '$remoteWheelhouse'; exit `$status"

    Write-Host "Installing from the uploaded wheelhouse..."
    ssh -o StrictHostKeyChecking=accept-new "${User}@${M10Host}" $installAndClean
    if ($LASTEXITCODE -ne 0) {
        Write-Error "The M10 rejected the downloaded wheel set. Review the pip error above."
        exit 2
    }

    Write-Host "Installed $Package for M10 Python $pythonVersion." -ForegroundColor Green
} finally {
    if ($deleteLocalWheelhouse -and (Test-Path -LiteralPath $localWheelhouse)) {
        $tempRoot = [IO.Path]::GetFullPath([IO.Path]::GetTempPath())
        $resolvedWheelhouse = [IO.Path]::GetFullPath($localWheelhouse)
        $leaf = Split-Path $resolvedWheelhouse -Leaf
        if ($resolvedWheelhouse.StartsWith($tempRoot, [StringComparison]::OrdinalIgnoreCase) -and
            $leaf.StartsWith("unihiker-m10-wheels-", [StringComparison]::OrdinalIgnoreCase)) {
            Remove-Item -LiteralPath $resolvedWheelhouse -Recurse -Force
        }
    }
}
