param(
    [switch]$Live
)

$ErrorActionPreference = "Stop"

if ([Environment]::OSVersion.Platform -ne [PlatformID]::Win32NT) {
    throw "This smoke test must run on Windows."
}
if (-not [Environment]::Is64BitOperatingSystem) {
    throw "Tencent Meeting CLI currently requires Windows x64 for this Skill."
}

$skillRoot = Split-Path -Parent $PSScriptRoot
$testScript = Join-Path $PSScriptRoot "test_watch_meeting_conflicts.py"
$requirements = Join-Path $PSScriptRoot "requirements.txt"

$pyLauncher = Get-Command "py.exe" -ErrorAction SilentlyContinue
if ($null -ne $pyLauncher) {
    $pythonExe = $pyLauncher.Source
    $pythonPrefix = @("-3")
} else {
    $python = Get-Command "python.exe" -ErrorAction Stop
    $pythonExe = $python.Source
    $pythonPrefix = @()
}

function Invoke-Python {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$PythonArguments)
    & $pythonExe @pythonPrefix @PythonArguments
    if ($LASTEXITCODE -ne 0) {
        throw "Python command failed with exit code $LASTEXITCODE."
    }
}

Invoke-Python "-c" "import sys; assert sys.version_info >= (3, 9), 'Python 3.9+ is required'; print(sys.version)"

try {
    Invoke-Python "-c" "from zoneinfo import ZoneInfo; ZoneInfo('Asia/Shanghai'); print('IANA timezone data: OK')"
} catch {
    throw "IANA timezone data is unavailable. Run: py -3 -m pip install -r `"$requirements`""
}

$tmeet = Get-Command "tmeet.cmd" -ErrorAction SilentlyContinue
if ($null -eq $tmeet) {
    $tmeet = Get-Command "tmeet.exe" -ErrorAction SilentlyContinue
}
if ($null -eq $tmeet) {
    throw "tmeet was not found. Run: npm install -g @tencentcloud/tmeet"
}

& $tmeet.Source "-V"
if ($LASTEXITCODE -ne 0) {
    throw "tmeet version check failed with exit code $LASTEXITCODE."
}

Invoke-Python $testScript

if ($Live) {
    & $tmeet.Source "auth" "status"
    if ($LASTEXITCODE -ne 0) {
        throw "tmeet is not logged in. Run tmeet auth login in the foreground."
    }

    $start = (Get-Date).ToString("o")
    $end = (Get-Date).AddDays(14).ToString("o")
    & $tmeet.Source "meeting" "list" "--start" $start "--end" $end "--show-all-sub" "1" "--compact"
    if ($LASTEXITCODE -ne 0) {
        throw "Live meeting-list smoke test failed with exit code $LASTEXITCODE."
    }
}

Write-Host "Windows x64 smoke test passed for: $skillRoot"
