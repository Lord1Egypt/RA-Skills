$ErrorActionPreference = "Stop"
$SkillDir = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$ConfigPath = Join-Path $SkillDir "config.json"
$WatchScript = Join-Path $PSScriptRoot "watch.ps1"

Write-Host "=== record2note Install ==="

# Check config
if (-not (Test-Path $ConfigPath)) {
    Write-Host "Error: config not found at $ConfigPath"
    Write-Host "Run the record2note skill setup first."
    exit 1
}

# Read config
$config = Get-Content $ConfigPath -Raw | ConvertFrom-Json
$whisperBin = if ($null -ne $config.whisper_binary) { $config.whisper_binary } else { "whisper-cli" }
$diarization = if ($null -ne $config.diarization) { $config.diarization } else { $true }

# Check prerequisites
$missing = @()
if (-not (Get-Command $whisperBin -ErrorAction SilentlyContinue)) { $missing += $whisperBin }
if (-not (Get-Command ffprobe -ErrorAction SilentlyContinue)) { $missing += "ffmpeg (ffprobe)" }
if (-not (Get-Command python3 -ErrorAction SilentlyContinue)) { $missing += "python3" }

if ($missing.Count -gt 0) {
    Write-Host "Missing dependencies:"
    foreach ($dep in $missing) {
        Write-Host "  - $dep"
    }
    Write-Host ""
    Write-Host "Install guides:"
    Write-Host "  whisper.cpp: https://github.com/ggerganov/whisper.cpp/releases"
    Write-Host "  ffmpeg: choco install ffmpeg"
    Write-Host "  python3: choco install python"
    exit 1
}

# Check pyannote if diarization enabled
if ($diarization) {
    python3 -c "import pyannote.audio" 2>$null
    if (-not $?) {
        Write-Host "Error: pyannote-audio not installed."
        Write-Host "Run: pip install pyannote-audio torch"
        Write-Host "And: huggingface-cli login"
        exit 1
    }
}

# Register Task Scheduler for watch mode
Write-Host "Registering scheduled task..."

# Expand the absolute path now (don't rely on $PSScriptRoot at runtime)
$watchScriptAbs = (Resolve-Path $WatchScript).Path

$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-WindowStyle Hidden -ExecutionPolicy Bypass -File `"$watchScriptAbs`""
$trigger = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1)
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive

# Remove existing task if present
Unregister-ScheduledTask -TaskName "record2note-watch" -Confirm:$false -ErrorAction SilentlyContinue

Register-ScheduledTask -TaskName "record2note-watch" -Action $action -Trigger $trigger -Settings $settings -Principal $principal | Out-Null

# Start the task immediately
Start-ScheduledTask -TaskName "record2note-watch"

Write-Host ""
Write-Host "=== Install complete ==="
Write-Host "Watch service is running in the background."
Write-Host "Log: $env:TEMP\record2note-watch.log"
Write-Host "To test: drop an audio file into your watch directory."
