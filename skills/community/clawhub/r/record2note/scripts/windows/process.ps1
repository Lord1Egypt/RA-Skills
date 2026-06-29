param(
    [string]$InputFile,
    [switch]$Watch
)

$ErrorActionPreference = "Stop"
$SkillDir = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$ConfigPath = Join-Path $SkillDir "config.json"
$HelperPath = Join-Path $SkillDir "scripts\common\read_config.py"
$DepsPath = Join-Path $SkillDir "scripts\common\deps_manager.py"

$Record2NoteBin = Join-Path $env:USERPROFILE ".config\record2note\bin"
if (Test-Path $Record2NoteBin) {
    $env:PATH = "$Record2NoteBin;$env:PATH"
}

# Read all config values in a single Python call
$configOutput = python3 $HelperPath shell $ConfigPath
$config = @{}
foreach ($line in $configOutput) {
    $idx = $line.IndexOf('=')
    if ($idx -gt 0) {
        $key = $line.Substring(0, $idx)
        $val = $line.Substring($idx + 1).TrimStart('"').TrimEnd('"')
        $config[$key] = $val
    }
}

$watchDir = [System.Environment]::ExpandEnvironmentVariables($config["watch_dir"])
$archiveDir = [System.Environment]::ExpandEnvironmentVariables($config["archive_dir"])
$obsidianVault = [System.Environment]::ExpandEnvironmentVariables($config["obsidian_vault"])
$obsidianSubdir = $config["obsidian_subdir"]
$whisperBin = $config["whisper_binary"]
$whisperModel = $config["whisper_model"]
$whisperModelPath = [System.Environment]::ExpandEnvironmentVariables($config["whisper_model_path"])
$syncMethod = $config["sync_method"]
$syncDelayIcloud = [int]$config["sync_delay_icloud"]
$syncDelaySyncthing = [int]$config["sync_delay_syncthing"]
$syncDelayManual = [int]$config["sync_delay_manual"]
$speakerCount = [int]$config["speaker_count"]
$language = $config["language"]
$diarization = $config["diarization"] -eq "true"
$denoise = $config["denoise"] -eq "true"
$vad = $config["vad"] -eq "true"
$vadModelPath = [System.Environment]::ExpandEnvironmentVariables($config["vad_model_path"])
$agentCli = $config["agent_cli"]
$noteMode = $config["note_mode"]
$obsidianIndex = $config["obsidian_index"]

# Ensure L1 dependencies (whisper binary, model, ffmpeg)
$ensureResult = python3 $DepsPath ensure L1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[record2note] Error: Required dependencies missing and could not be auto-installed." -ForegroundColor Red
    Write-Host "[record2note] Run: python3 $DepsPath check  (to see what's missing)"
    exit 1
}

# Watch mode
if ($Watch) {
    Write-Host "[record2note] Watching: $watchDir"

    $watcher = New-Object System.IO.FileSystemWatcher
    $watcher.Path = $watchDir
    $watcher.Filter = "*.*"
    $watcher.IncludeSubdirectories = $false
    $watcher.EnableRaisingEvents = $true

    $scriptPath = $PSCommandPath
    $skillDir = $SkillDir
    $configFile = $ConfigPath

    $action = {
        $path = $Event.SourceEventArgs.FullPath
        $ext = [System.IO.Path]::GetExtension($path).ToLower()
        if ($ext -in @('.m4a', '.wav', '.mp3', '.aac', '.ogg') -and (Test-Path $path -PathType Leaf)) {
            $basename = [System.IO.Path]::GetFileName($path)
            
            # Lock file check (prevent duplicate processing)
            $lockDir = Join-Path ([Environment]::GetFolderPath("LocalApplicationData")) "record2note\locks"
            New-Item -ItemType Directory -Path $lockDir -Force | Out-Null
            $lockFile = Join-Path $lockDir "$basename.lock"
            if (Test-Path $lockFile) { return }
            
            # Stability check (wait for file to finish writing/syncing)
            $firstSize = (Get-Item $path).Length
            Start-Sleep -Seconds 5
            if (-not (Test-Path $path)) { return }
            $secondSize = (Get-Item $path).Length
            if ($firstSize -ne $secondSize -or $secondSize -eq 0) { return }
            
            # Create lock and process
            New-Item -ItemType File -Path $lockFile -Force | Out-Null
            Write-Host "[record2note] New file detected: $basename"
            # Log queue status: count audio files still in watch dir
            $audioExts = @('.m4a','.wav','.mp3','.aac','.ogg')
            $queueFiles = Get-ChildItem -Path $watchDir -File | Where-Object { $audioExts -contains $_.Extension.ToLower() }
            $queueCount = @($queueFiles).Count
            if ($queueCount -gt 1) {
                Write-Host "[record2note] Queue: $queueCount files waiting to be processed"
            }
            & powershell -NoProfile -ExecutionPolicy Bypass -File $using:scriptPath -InputFile $path
            Remove-Item -Force $lockFile -ErrorAction SilentlyContinue
        }
    }

    Register-ObjectEvent $watcher "Created" -Action $action | Out-Null
    Write-Host "[record2note] FileSystemWatcher active. Press Ctrl+C to stop."
    while ($true) { Start-Sleep -Seconds 1 }
    exit 0
}

if (-not $InputFile) {
    Write-Host "Usage: process.ps1 -InputFile <audio_file> or process.ps1 -Watch"
    exit 1
}

# Speaker labels for English notes
$speakerLabels = @("Speaker A","Speaker B","Speaker C","Speaker D","Speaker E","Speaker F","Speaker G","Speaker H","Speaker I","Speaker J")

$basename = [System.IO.Path]::GetFileName($InputFile)
$filenameNoExt = [System.IO.Path]::GetFileNameWithoutExtension($InputFile)
$dateStr = Get-Date -Format "yyyy-MM-dd"
$workDir = Join-Path ([System.IO.Path]::GetTempPath()) ([System.Guid]::NewGuid().ToString())
New-Item -ItemType Directory -Path $workDir | Out-Null

function Convert-ToWav {
    param(
        [string]$InputFile,
        [string]$OutputFile,
        [bool]$DoDenoise
    )
    
    if ($DoDenoise) {
        Write-Host "[record2note] Converting to WAV with noise reduction..."
        & ffmpeg -i $InputFile -ar 16000 -ac 1 -c:a pcm_s16le -af "afftdn=nf=-25" $OutputFile -y 2>&1 | Select-Object -Last 5
    } else {
        Write-Host "[record2note] Converting to WAV..."
        & ffmpeg -i $InputFile -ar 16000 -ac 1 -c:a pcm_s16le $OutputFile -y 2>&1 | Select-Object -Last 5
    }
}

function Invoke-Whisper {
    param(
        [string]$AudioFile,
        [string]$ModelPath,
        [string]$Language,
        [string]$OutputDir,
        [string]$WhisperBin,
        [bool]$VadEnabled,
        [string]$VadModelPath
    )
    
    $vadArgs = @()
    if ($VadEnabled) {
        if (Test-Path $VadModelPath) {
            $vadArgs = @("--vad", "-vm", $VadModelPath)
            Write-Host "[record2note] VAD enabled"
        } else {
            Write-Host "[record2note] VAD model not found at $VadModelPath, skipping VAD"
        }
    }

    # Attempt 1: Default (full GPU)
    Write-Host "[record2note] Whisper attempt 1/4 (GPU)..."
    & $WhisperBin -f $AudioFile -m $ModelPath -osrt --language $Language $vadArgs -of "$OutputDir\transcript" 2>&1
    if ($LASTEXITCODE -eq 0) { return $true }
    
    # Attempt 2: Disable flash attention
    Write-Host "[record2note] Whisper attempt 2/4 (GPU, -nfa)..."
    & $WhisperBin -f $AudioFile -m $ModelPath -osrt --language $Language -nfa $vadArgs -of "$OutputDir\transcript" 2>&1
    if ($LASTEXITCODE -eq 0) { return $true }
    
    # Attempt 3: Disable flash attention + reduce threads
    Write-Host "[record2note] Whisper attempt 3/4 (GPU, -nfa -t 2)..."
    & $WhisperBin -f $AudioFile -m $ModelPath -osrt --language $Language -nfa -t 2 $vadArgs -of "$OutputDir\transcript" 2>&1
    if ($LASTEXITCODE -eq 0) { return $true }
    
    # Attempt 4: CPU fallback
    Write-Host "[record2note] Whisper attempt 4/4 (CPU fallback)..."
    & $WhisperBin -f $AudioFile -m $ModelPath -osrt --language $Language -ng $vadArgs -of "$OutputDir\transcript" 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Whisper transcription failed on CPU fallback (exit code: $LASTEXITCODE)"
    }
}

try {
    Write-Host "[record2note] Processing: $InputFile"

    # Step 1: Wait for sync
    if ($syncMethod -eq "icloud") {
        Write-Host "[record2note] iCloud mode: waiting ${syncDelayIcloud}s..."
        Start-Sleep -Seconds $syncDelayIcloud
    } elseif ($syncMethod -eq "syncthing") {
        Write-Host "[record2note] Syncthing mode: waiting ${syncDelaySyncthing}s..."
        Start-Sleep -Seconds $syncDelaySyncthing
    } else {
        Write-Host "[record2note] Manual mode: waiting ${syncDelayManual}s..."
        Start-Sleep -Seconds $syncDelayManual
    }

    # Step 2: Get audio duration
    $duration = "00:00:00"
    try {
        $ffprobeOut = & ffprobe -i $InputFile -show_entries format=duration -v quiet -of csv="p=0" 2>$null
        if ($ffprobeOut) {
            $seconds = [double]$ffprobeOut
            $h = [int]([math]::Floor($seconds / 3600))
            $m = [int]([math]::Floor(($seconds % 3600) / 60))
            $s = [int]($seconds % 60)
            $duration = "{0:D2}:{1:D2}:{2:D2}" -f $h, $m, $s
        }
    } catch {
        Write-Host "[record2note] Warning: ffprobe failed, skipping duration"
    }

    # Step 3: Convert to WAV (with optional denoising)
    $wavFile = Join-Path $workDir "audio.wav"
    Convert-ToWav -InputFile $InputFile -OutputFile $wavFile -DoDenoise $denoise

    # Step 4: Run whisper with GPU fallback
    Write-Host "[record2note] Transcribing with $whisperBin..."
    $modelFile = Join-Path $whisperModelPath $whisperModel
    Invoke-Whisper -AudioFile $wavFile -ModelPath $modelFile -Language $language -OutputDir $workDir -WhisperBin $whisperBin -VadEnabled $vad -VadModelPath $vadModelPath

    # Step 5: Diarization (optional)
    $speakerNames = "N/A"
    if ($diarization) {
        $depsResult = python3 $DepsPath ensure L3 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-Host "[record2note] Warning: Diarization dependencies not available, skipping diarization."
            $diarization = $false
        } else {
            Write-Host "[record2note] Running speaker diarization..."
            $diarizeScript = Join-Path $SkillDir "scripts\common\diarize.py"
            & python3 $diarizeScript $InputFile $speakerCount | Out-File -FilePath "$workDir\diarization.json" -Encoding utf8

            $speakerNames = python3 $HelperPath speaker_names $workDir $language
        }
    }

    # Step 6: Merge SRT + diarization
    Write-Host "[record2note] Merging transcript..."
    python3 $HelperPath merge $workDir $(if ($diarization) { "true" } else { "false" })

    # Step 7: Save result to pending directory for agent to process
    $pendingDir = Join-Path $archiveDir "pending"
    New-Item -ItemType Directory -Path $pendingDir -Force | Out-Null
    $resultFile = Join-Path $pendingDir "${dateStr}_${filenameNoExt}.json"

    $metadata = @{
        title_candidate = $filenameNoExt
        date = $dateStr
        duration = $duration
        source = $InputFile
        speakers = $speakerNames
        language = $language
        diarization = $diarization
        note_mode = $noteMode
        obsidian_index = $obsidianIndex
    }
    $transcriptContent = Get-Content "$workDir\raw_transcript.md" -Raw -Encoding utf8
    $result = @{ metadata = $metadata; transcript = $transcriptContent }
    $result | ConvertTo-Json -Depth 10 | Out-File -FilePath $resultFile -Encoding utf8
    Write-Host "[record2note] Result saved to pending: $resultFile"

    # Step 7a: Trigger agent CLI if configured
    $triggerScript = Join-Path $SkillDir "scripts\common\trigger_agent.sh"
    if (Test-Path $triggerScript) {
        & bash $triggerScript $resultFile $agentCli $SkillDir 2>$null
    }

    # Step 8: Output metadata and transcript for agent processing
    Write-Host "[record2note] METADATA_START"
    Write-Host "TITLE_CANDIDATE=$filenameNoExt"
    Write-Host "DATE=$dateStr"
    Write-Host "DURATION=$duration"
    Write-Host "SOURCE=$InputFile"
    Write-Host "SPEAKERS=$speakerNames"
    Write-Host "LANGUAGE=$language"
    Write-Host "DIARIZATION=$diarization"
    Write-Host "METADATA_END"

    Write-Host "[record2note] TRANSCRIPT_START"
    Write-Host $transcriptContent
    Write-Host ""
    Write-Host "[record2note] TRANSCRIPT_END"

    Write-Host "[record2note] Transcription complete. Result saved to pending directory."

} finally {
    # Keep workDir for agent processing; OS temp directory will clean up eventually
}
