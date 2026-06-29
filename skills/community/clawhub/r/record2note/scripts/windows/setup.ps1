param(
    [string]$WatchDir = "$HOME\Recordings\raw",
    [string]$ArchiveDir = "$HOME\Recordings\archive",
    [Parameter(Mandatory=$true)][string]$Vault,
    [string]$Subdir = "Journal\Transcripts",
    [string]$WhisperBin = "whisper-cli",
    [string]$Model = "ggml-base.bin",
    [string]$ModelPath = "$HOME\whisper-models",
    [string]$Sync = "syncthing",
    [int]$SyncDelayIcloud = 60,
    [int]$SyncDelaySyncthing = 10,
    [int]$SyncDelayManual = 10,
    [int]$Speakers = 0,
    [string]$Language = "en",
    [bool]$Diarization = $true,
    [bool]$Denoise = $true,
    [bool]$Vad = $false,
    [string]$VadModelPath = "$HOME\whisper-models\ggml-silero-v6.2.0.bin",
    [string]$Mirror = "auto",
    [string]$IcloudWatchSubdir = "VoiceRecordings",
    [string]$AgentCli = "auto",
    [string]$NoteMode = "markdown",
    [string]$ObsidianIndex = "Recording Index"
)

$ErrorActionPreference = "Stop"

$SkillDir = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$ConfigFile = Join-Path $SkillDir "config.json"

# Create directories
New-Item -ItemType Directory -Path $WatchDir -Force | Out-Null
New-Item -ItemType Directory -Path $ArchiveDir -Force | Out-Null

# Write config
$config = @{
    platform = "windows"
    watch_dir = $WatchDir
    archive_dir = $ArchiveDir
    obsidian_vault = $Vault
    obsidian_subdir = $Subdir
    whisper_binary = $WhisperBin
    whisper_model = $Model
    whisper_model_path = $ModelPath
    sync_method = $Sync
    sync_delay_icloud = $SyncDelayIcloud
    sync_delay_syncthing = $SyncDelaySyncthing
    sync_delay_manual = $SyncDelayManual
    icloud_watch_subdir = $IcloudWatchSubdir
    agent_cli = $AgentCli
    note_mode = $NoteMode
    obsidian_index = $ObsidianIndex
    speaker_count = $Speakers
    language = $Language
    diarization = $Diarization
    denoise = $Denoise
    vad = $Vad
    vad_model_path = $VadModelPath
    mirror = $Mirror
}

$config | ConvertTo-Json -Depth 10 | Out-File -FilePath $ConfigFile -Encoding utf8

Write-Host ""
Write-Host "=== Sync Setup Guidance ==="
switch ($Sync) {
    "syncthing" {
        Write-Host "Syncthing sync mode:"
        Write-Host "  Watch directory: $WatchDir"
        Write-Host "  File flow: phone -> Syncthing -> watch_dir -> transcription -> local archive"
        Write-Host ""
        Write-Host "  First-time setup steps:"
        Write-Host "    1. Download Syncthing: https://syncthing.net/downloads/"
        Write-Host "    2. Run syncthing.exe on the computer and open http://127.0.0.1:8384 in a browser"
        Write-Host "    3. Install Syncthing App on Android or Mobius Sync on iOS"
        Write-Host "    4. Add each device to the other: Actions -> Show ID -> paste the other device ID"
        Write-Host "    5. Add the folder on the computer: $WatchDir -> share it with the phone"
        Write-Host "    6. Confirm the share on the phone and set the local folder to the recordings directory"
        Write-Host "  Wait time: ${SyncDelaySyncthing}s"
    }
    "icloud" {
        Write-Host "iCloud Drive sync mode:"
        Write-Host "  Watch directory: $WatchDir"
        Write-Host "  Prerequisite: install iCloud for Windows (Microsoft Store)"
        Write-Host "  File flow: iPhone -> iCloud -> iCloud Drive/$IcloudWatchSubdir -> watch_dir -> transcription -> local archive"
        Write-Host "  Wait time: ${SyncDelayIcloud}s"
    }
    "manual" {
        Write-Host "Manual mode:"
        Write-Host "  Watch directory: $WatchDir"
        Write-Host "  Usage:"
        Write-Host "    - Copy the phone recording files to $WatchDir over USB"
        Write-Host "    - Or import them through cloud drives or shared folders"
        Write-Host "    - Or specify the file path directly when processing a recording"
        Write-Host "  Wait time: ${SyncDelayManual}s"
    }
}

Write-Host "[record2note] Setup complete."
Write-Host "  Config: $ConfigFile"
Write-Host "  Watch: $WatchDir"
Write-Host "  Archive: $ArchiveDir"
Write-Host ""
Write-Host "Dependencies:"
Write-Host "  Run: python3 $SkillDir\scripts\common\deps_manager.py ensure L1"
Write-Host "  Or process an audio file - dependencies will auto-install on first use."
