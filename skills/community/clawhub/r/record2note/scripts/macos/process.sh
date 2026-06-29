#!/bin/bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
CONFIG="$SKILL_DIR/config.json"
HELPER="$SKILL_DIR/scripts/common/read_config.py"
DEPS="$SKILL_DIR/scripts/common/deps_manager.py"

RECORD2NOTE_BIN="$HOME/.config/record2note/bin"
if [ -d "$RECORD2NOTE_BIN" ]; then
    export PATH="$RECORD2NOTE_BIN:/opt/local/bin:$PATH"
fi

# Read all config values in a single Python call
eval "$(python3 "$HELPER" shell "$CONFIG")"

# Expand ~ in path values
expand_path() {
    echo "${1/#\~/$HOME}"
}
watch_dir=$(expand_path "$watch_dir")
archive_dir=$(expand_path "$archive_dir")
obsidian_vault=$(expand_path "$obsidian_vault")
whisper_model_path=$(expand_path "$whisper_model_path")
vad_model_path=$(expand_path "$vad_model_path")

# Ensure L1 dependencies (whisper binary, model, ffmpeg)
if ! python3 "$DEPS" ensure L1; then
    echo "[record2note] Error: Required dependencies missing and could not be auto-installed." >&2
    echo "[record2note] Run: python3 $DEPS check  (to see what's missing)" >&2
    exit 1
fi

# --watch mode
if [ "${1:-}" = "--watch" ]; then
    echo "[record2note] Watching: $watch_dir"
    if [ "$sync_method" = "icloud" ]; then
        LOCK_DIR="$HOME/.cache/record2note/locks"
        mkdir -p "$LOCK_DIR"
    else
        LOCK_DIR="$watch_dir/.record2note_locks"
        mkdir -p "$LOCK_DIR"
    fi

    is_icloud_ready() {
        local file="$1"
        if [ ! -f "$file" ] || [ ! -s "$file" ]; then
            return 1
        fi
        if xattr -p com.apple.fileprovider.placeholder "$file" &>/dev/null 2>&1; then
            return 1
        fi
        return 0
    }

    fswatch -0 "$watch_dir" | while IFS= read -d "" event; do
        case "$event" in
            *.m4a|*.M4A|*.wav|*.WAV|*.mp3|*.MP3|*.aac|*.AAC|*.ogg|*.OGG)
                if [ -f "$event" ]; then
                    # Use lock file to prevent duplicate processing
                    LOCK_FILE="$LOCK_DIR/$(basename "$event").lock"
                    if [ -f "$LOCK_FILE" ]; then
                        continue
                    fi

                    # Wait for file to stabilize
                    if [ "$sync_method" = "icloud" ]; then
                        if ! is_icloud_ready "$event"; then
                            continue
                        fi
                        first_size=$(stat -f %z "$event" 2>/dev/null || echo "0")
                        sleep 10
                        if ! is_icloud_ready "$event"; then
                            continue
                        fi
                        second_size=$(stat -f %z "$event" 2>/dev/null || echo "0")
                        if [ "$first_size" != "$second_size" ] || [ "$second_size" = "0" ]; then
                            continue
                        fi
                    else
                        first_size=$(stat -f %z "$event" 2>/dev/null || echo "0")
                        sleep 3
                        if [ ! -f "$event" ]; then
                            rm -f "$LOCK_FILE"
                            continue
                        fi
                        second_size=$(stat -f %z "$event" 2>/dev/null || echo "0")
                        if [ "$first_size" != "$second_size" ] || [ "$second_size" = "0" ]; then
                            continue
                        fi
                    fi

                    # Create lock and process
                    touch "$LOCK_FILE"
                    # Log queue status: count audio files still in watch dir
                    shopt -s nullglob
                    queue_count=0
                    for _ in "$watch_dir"/*.m4a "$watch_dir"/*.M4A "$watch_dir"/*.wav "$watch_dir"/*.WAV "$watch_dir"/*.mp3 "$watch_dir"/*.MP3 "$watch_dir"/*.aac "$watch_dir"/*.AAC "$watch_dir"/*.ogg "$watch_dir"/*.OGG; do
                        queue_count=$((queue_count + 1))
                    done
                    shopt -u nullglob
                    if [ "$queue_count" -gt 1 ]; then
                        echo "[record2note] Queue: $queue_count files waiting to be processed"
                    fi
                    "$0" "$event" 2>&1
                    rm -f "$LOCK_FILE"
                fi
                ;;
        esac
    done
    exit 0
fi

if [ -z "${1:-}" ]; then
    echo "Usage: process.sh <audio_file> or process.sh --watch"
    exit 1
fi

# Speaker labels for English notes
SPEAKER_LABELS="['Speaker A','Speaker B','Speaker C','Speaker D','Speaker E','Speaker F','Speaker G','Speaker H','Speaker I','Speaker J']"

INPUT_FILE="$1"
BASENAME=$(basename "$INPUT_FILE")
FILENAME_NOEXT="${BASENAME%.*}"
DATE_STR=$(date +%Y-%m-%d)
WORKDIR=$(mktemp -d)
# Keep WORKDIR for agent processing; OS temp directory will clean up eventually

echo "[record2note] Processing: $INPUT_FILE"

# Helper: Run a command with timeout (macOS has no timeout command)
run_with_timeout() {
    local timeout_secs="$1"; shift
    "$@" &
    local cmd_pid=$!
    (sleep "$timeout_secs"; kill "$cmd_pid" 2>/dev/null) &
    local killer_pid=$!
    wait "$cmd_pid" 2>/dev/null
    local exit_code=$?
    kill "$killer_pid" 2>/dev/null
    return $exit_code
}

# Helper: Convert seconds to human-readable format
format_duration() {
    local secs="$1"
    printf '%dh%02dm%02ds' $((secs/3600)) $((secs%3600/60)) $((secs%60))
}

# Helper: Convert audio to WAV format suitable for whisper (16kHz, mono, 16-bit)
convert_to_wav() {
    local input="$1"
    local output="$2"
    local do_denoise="$3"
    
    if [ "$do_denoise" = "True" ] || [ "$do_denoise" = "true" ]; then
        echo "[record2note] Converting to WAV with noise reduction..."
        ffmpeg -i "$input" -ar 16000 -ac 1 -c:a pcm_s16le -af "afftdn=nf=-25" "$output" -y 2>&1 | tail -5
    else
        echo "[record2note] Converting to WAV..."
        ffmpeg -i "$input" -ar 16000 -ac 1 -c:a pcm_s16le "$output" -y 2>&1 | tail -5
    fi
}

# Helper: Run whisper with progressive GPU degradation
# $1=audio_file $2=model_path $3=language $4=output_dir $5=whisper_binary
# $6=vad_enabled $7=vad_model_path $8=timeout_seconds
run_whisper() {
    local audio_file="$1"
    local model_path="$2"
    local language="$3"
    local output_dir="$4"
    local whisper_binary="$5"
    local vad_enabled="$6"
    local vad_model_path="$7"
    local timeout_secs="${8:-1800}"

    local vad_extra=""
    if [ "$vad_enabled" = "True" ] || [ "$vad_enabled" = "true" ]; then
        if [ -f "$vad_model_path" ]; then
            vad_extra="--vad -vm $vad_model_path"
            echo "[record2note] VAD enabled"
        else
            echo "[record2note] VAD model not found at $vad_model_path, skipping VAD"
        fi
    fi

    local timeout_display
    timeout_display=$(format_duration "$timeout_secs")
    echo "[record2note] Whisper timeout set to: $timeout_display"

    # Attempt 1: Default (full GPU)
    echo "[record2note] Whisper attempt 1/4 (GPU)..."
    if run_with_timeout "$timeout_secs" $whisper_binary -f "$audio_file" -m "$model_path" -osrt --language "$language" $vad_extra -of "$output_dir/transcript" 2>&1; then
        return 0
    fi

    # Attempt 2: Disable flash attention (reduce peak GPU memory)
    echo "[record2note] Whisper attempt 2/4 (GPU, no flash attention)..."
    if run_with_timeout "$timeout_secs" $whisper_binary -f "$audio_file" -m "$model_path" -osrt --language "$language" -nfa $vad_extra -of "$output_dir/transcript" 2>&1; then
        return 0
    fi

    # Attempt 3: Disable flash attention + reduce threads
    echo "[record2note] Whisper attempt 3/4 (GPU, -nfa -t 2)..."
    if run_with_timeout "$timeout_secs" $whisper_binary -f "$audio_file" -m "$model_path" -osrt --language "$language" -nfa -t 2 $vad_extra -of "$output_dir/transcript" 2>&1; then
        return 0
    fi

    # Attempt 4: CPU fallback (guaranteed to work)
    echo "[record2note] Whisper attempt 4/4 (CPU fallback)..."
    run_with_timeout "$timeout_secs" $whisper_binary -f "$audio_file" -m "$model_path" -osrt --language "$language" -ng $vad_extra -of "$output_dir/transcript" 2>&1
}

# Step 1: Wait for file to finish syncing
if [ "$sync_method" = "icloud" ]; then
    echo "[record2note] iCloud mode: waiting ${sync_delay_icloud}s for sync..."
    sleep "$sync_delay_icloud"
elif [ "$sync_method" = "syncthing" ]; then
    echo "[record2note] Syncthing mode: waiting ${sync_delay_syncthing}s for sync..."
    sleep "$sync_delay_syncthing"
else
    echo "[record2note] Manual mode: waiting ${sync_delay_manual}s..."
    sleep "$sync_delay_manual"
fi

# Step 2: Get audio duration
duration=$(ffprobe -i "$INPUT_FILE" -show_entries format=duration -v quiet -of csv="p=0" 2>/dev/null || echo "0")
duration_formatted=$(python3 -c "
try:
    d = float($duration)
    if d < 0: d = 0
except (ValueError, TypeError):
    d = 0
h = int(d // 3600)
m = int((d % 3600) // 60)
s = int(d % 60)
print(f'{h:02d}:{m:02d}:{s:02d}')
")

# Step 3: Convert to WAV (with optional denoising)
WAV_FILE="$WORKDIR/audio.wav"
convert_to_wav "$INPUT_FILE" "$WAV_FILE" "$denoise"

# Step 3b: Calculate whisper timeout based on audio duration and model size
# Formula: multiplier × audio length + buffer
#   base:   3x (fastest)
#   medium: 5x
#   large:  8x (slowest)
# Buffer: 600s (model loading, fallback attempts)
whisper_timeout=$(python3 -c "
d = float('$duration') if '$duration' else 0
model = '$whisper_model'
if 'large' in model:
    multiplier = 8
elif 'medium' in model:
    multiplier = 5
else:
    multiplier = 3
timeout = int(d * multiplier + 600)
print(timeout)
")

# Step 4: Run whisper with GPU fallback
echo "[record2note] Transcribing with $whisper_binary..."
run_whisper "$WAV_FILE" "$whisper_model_path/$whisper_model" "$language" "$WORKDIR" "$whisper_binary" "$vad" "$vad_model_path" "$whisper_timeout"

# Step 5: Diarization (optional)
if [ "$diarization" = "True" ] || [ "$diarization" = "true" ]; then
    if ! python3 "$DEPS" ensure L3 2>/dev/null; then
        echo "[record2note] Warning: Diarization dependencies not available, skipping diarization." >&2
        diarization="false"
    else
        echo "[record2note] Running speaker diarization..."
        python3 "$SKILL_DIR/scripts/common/diarize.py" "$INPUT_FILE" "$speaker_count" > "$WORKDIR/diarization.json"

        SPEAKER_NAMES=$(python3 "$HELPER" speaker_names "$WORKDIR" "$language")
    fi
else
    echo "[record2note] Diarization disabled, skipping..."
    SPEAKER_NAMES="N/A"
fi

# Step 6: Merge SRT + diarization into raw Markdown
echo "[record2note] Merging transcript..."
python3 "$HELPER" merge "$WORKDIR" "$diarization"

# Step 7: Save result to pending directory for agent to process
PENDING_DIR="$(expand_path "$archive_dir")/pending"
mkdir -p "$PENDING_DIR"
RESULT_FILE="$PENDING_DIR/${DATE_STR}_${FILENAME_NOEXT}.json"

python3 - "$WORKDIR" "$RESULT_FILE" "$FILENAME_NOEXT" "$DATE_STR" "$duration_formatted" "$INPUT_FILE" "$SPEAKER_NAMES" "$language" "$diarization" "$note_mode" "$obsidian_index" << 'PYEOF'
import json, sys

workdir, result_file, title_candidate, date_str, duration_fmt, source_file, speakers, language, diarization, note_mode, obsidian_index = sys.argv[1:]

with open(f"{workdir}/raw_transcript.md", encoding="utf-8") as f:
    transcript = f.read()

metadata = {
    "title_candidate": title_candidate,
    "date": date_str,
    "duration": duration_fmt,
    "source": source_file,
    "speakers": speakers,
    "language": language,
    "diarization": diarization,
    "note_mode": note_mode,
    "obsidian_index": obsidian_index
}

with open(result_file, "w", encoding="utf-8") as f:
    json.dump({"metadata": metadata, "transcript": transcript}, f, ensure_ascii=False, indent=2)
print(f"[record2note] Result saved to pending: {result_file}")
PYEOF

# Step 7a: Trigger agent CLI if configured
TRIGGER="$SKILL_DIR/scripts/common/trigger_agent.sh"
if [ -x "$TRIGGER" ]; then
    "$TRIGGER" "$RESULT_FILE" "$agent_cli" "$SKILL_DIR" || true
fi

# Step 8: Output metadata and transcript for agent processing
echo "[record2note] METADATA_START"
echo "TITLE_CANDIDATE=$FILENAME_NOEXT"
echo "DATE=$DATE_STR"
echo "DURATION=$duration_formatted"
echo "SOURCE=$INPUT_FILE"
echo "SPEAKERS=$SPEAKER_NAMES"
echo "LANGUAGE=$language"
echo "DIARIZATION=$diarization"
echo "METADATA_END"

echo "[record2note] TRANSCRIPT_START"
cat "$WORKDIR/raw_transcript.md"
echo ""
echo "[record2note] TRANSCRIPT_END"

echo "[record2note] Transcription complete. Result saved to pending directory."
