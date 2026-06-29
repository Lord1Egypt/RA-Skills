#!/bin/bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/../.." && pwd)"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --watch-dir)    WATCH_DIR="$2"; shift 2 ;;
        --archive-dir)  ARCHIVE_DIR="$2"; shift 2 ;;
        --vault)        VAULT="$2"; shift 2 ;;
        --subdir)       SUBDIR="$2"; shift 2 ;;
        --model)        MODEL="$2"; shift 2 ;;
        --model-path)   MODEL_PATH="$2"; shift 2 ;;
        --sync)         SYNC_METHOD="$2"; shift 2 ;;
        --speakers)     SPEAKERS="$2"; shift 2 ;;
        --language)     LANGUAGE="$2"; shift 2 ;;
        --whisper-bin)  WHISPER_BIN="$2"; shift 2 ;;
        --sync-delay-icloud) SYNC_DELAY_ICLOUD="$2"; shift 2 ;;
        --sync-delay-syncthing) SYNC_DELAY_SYNCTHING="$2"; shift 2 ;;
        --sync-delay-manual) SYNC_DELAY_MANUAL="$2"; shift 2 ;;
        --icloud-watch-subdir) ICLOUD_WATCH_SUBDIR="$2"; shift 2 ;;
        --diarization)  DIARIZATION="$2"; shift 2 ;;
        --denoise)      DENOISE="$2"; shift 2 ;;
        --vad)          VAD="$2"; shift 2 ;;
        --vad-model-path) VAD_MODEL_PATH="$2"; shift 2 ;;
        --mirror)        MIRROR="$2"; shift 2 ;;
        --agent-cli)     AGENT_CLI="$2"; shift 2 ;;
        --note-mode)     NOTE_MODE="$2"; shift 2 ;;
        --obsidian-index) OBSIDIAN_INDEX="$2"; shift 2 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

# Defaults
ICLOUD_WATCH_SUBDIR="${ICLOUD_WATCH_SUBDIR:-VoiceRecordings}"
if [ -z "${WATCH_DIR:-}" ]; then
    if [ "${SYNC_METHOD:-icloud}" = "icloud" ]; then
        WATCH_DIR="$HOME/Library/Mobile Documents/com~apple~CloudDocs/$ICLOUD_WATCH_SUBDIR"
    else
        WATCH_DIR="$HOME/Recordings/raw"
    fi
fi
ARCHIVE_DIR="${ARCHIVE_DIR:-$HOME/Recordings/archive}"
VAULT="${VAULT:?--vault is required}"
SUBDIR="${SUBDIR:-Journal/Transcripts}"
MODEL="${MODEL:-ggml-base.bin}"
MODEL_PATH="${MODEL_PATH:-/usr/local/share/whisper-models}"
WHISPER_BIN="${WHISPER_BIN:-whisper-cli}"
SYNC_METHOD="${SYNC_METHOD:-icloud}"
SYNC_DELAY_ICLOUD="${SYNC_DELAY_ICLOUD:-60}"
SYNC_DELAY_SYNCTHING="${SYNC_DELAY_SYNCTHING:-10}"
SYNC_DELAY_MANUAL="${SYNC_DELAY_MANUAL:-10}"
SPEAKERS="${SPEAKERS:-0}"
LANGUAGE="${LANGUAGE:-en}"
DIARIZATION="${DIARIZATION:-true}"
DENOISE="${DENOISE:-true}"
VAD="${VAD:-false}"
VAD_MODEL_PATH="${VAD_MODEL_PATH:-$MODEL_PATH/ggml-silero-v6.2.0.bin}"
MIRROR="${MIRROR:-auto}"
AGENT_CLI="${AGENT_CLI:-auto}"
NOTE_MODE="${NOTE_MODE:-markdown}"
OBSIDIAN_INDEX="${OBSIDIAN_INDEX:-Recording Index}"


CONFIG_FILE="$SKILL_DIR/config.json"

# Create directories
mkdir -p "$WATCH_DIR" "$ARCHIVE_DIR"

# Write config
export CFG_WATCH_DIR="$WATCH_DIR"
export CFG_ARCHIVE_DIR="$ARCHIVE_DIR"
export CFG_VAULT="$VAULT"
export CFG_SUBDIR="$SUBDIR"
export CFG_MODEL="$MODEL"
export CFG_MODEL_PATH="$MODEL_PATH"
export CFG_WHISPER_BIN="$WHISPER_BIN"
export CFG_SYNC="$SYNC_METHOD"
export CFG_SYNC_DELAY_ICLOUD="$SYNC_DELAY_ICLOUD"
export CFG_SYNC_DELAY_SYNCTHING="$SYNC_DELAY_SYNCTHING"
export CFG_SYNC_DELAY_MANUAL="$SYNC_DELAY_MANUAL"
export CFG_SPEAKERS="$SPEAKERS"
export CFG_LANG="$LANGUAGE"
export CFG_DIARIZATION="$DIARIZATION"
export CFG_DENOISE="$DENOISE"
export CFG_VAD="$VAD"
export CFG_VAD_MODEL_PATH="$VAD_MODEL_PATH"
export CFG_MIRROR="$MIRROR"
export CFG_AGENT_CLI="$AGENT_CLI"
export CFG_NOTE_MODE="$NOTE_MODE"
export CFG_OBSIDIAN_INDEX="$OBSIDIAN_INDEX"
export CFG_ICLOUD_WATCH_SUBDIR="$ICLOUD_WATCH_SUBDIR"
export CFG_PLATFORM="macos"
export CFG_FILE="$CONFIG_FILE"

python3 << 'PYEOF'
import json, os

diarization = os.environ["CFG_DIARIZATION"].lower() in ("true", "1", "yes")
denoise = os.environ["CFG_DENOISE"].lower() in ("true", "1", "yes")
vad = os.environ["CFG_VAD"].lower() in ("true", "1", "yes")

config = {
    "platform": os.environ["CFG_PLATFORM"],
    "watch_dir": os.environ["CFG_WATCH_DIR"],
    "archive_dir": os.environ["CFG_ARCHIVE_DIR"],
    "obsidian_vault": os.environ["CFG_VAULT"],
    "obsidian_subdir": os.environ["CFG_SUBDIR"],
    "whisper_binary": os.environ["CFG_WHISPER_BIN"],
    "whisper_model": os.environ["CFG_MODEL"],
    "whisper_model_path": os.environ["CFG_MODEL_PATH"],
    "sync_method": os.environ["CFG_SYNC"],
    "sync_delay_icloud": int(os.environ["CFG_SYNC_DELAY_ICLOUD"]),
    "sync_delay_syncthing": int(os.environ["CFG_SYNC_DELAY_SYNCTHING"]),
    "sync_delay_manual": int(os.environ["CFG_SYNC_DELAY_MANUAL"]),
    "speaker_count": int(os.environ["CFG_SPEAKERS"]),
    "language": os.environ["CFG_LANG"],
    "diarization": diarization,
    "denoise": denoise,
    "vad": vad,
    "vad_model_path": os.environ["CFG_VAD_MODEL_PATH"],
    "mirror": os.environ["CFG_MIRROR"],
    "agent_cli": os.environ["CFG_AGENT_CLI"],
    "icloud_watch_subdir": os.environ["CFG_ICLOUD_WATCH_SUBDIR"],
    "note_mode": os.environ["CFG_NOTE_MODE"],
    "obsidian_index": os.environ["CFG_OBSIDIAN_INDEX"]
}
with open(os.environ["CFG_FILE"], "w", encoding="utf-8") as f:
    json.dump(config, f, indent=2, ensure_ascii=False)
print("Config written to: " + os.environ["CFG_FILE"])
PYEOF

echo "[record2note] Setup complete."
echo "  Config: $CONFIG_FILE"
echo "  Watch: $WATCH_DIR"
echo "  Archive: $ARCHIVE_DIR"
echo ""

# Sync setup guidance
echo "=== Sync Setup Guidance ==="
case "$SYNC_METHOD" in
    icloud)
        echo "iCloud Drive sync mode:"
        echo "  Watch directory: $WATCH_DIR"
        echo "  File flow: iPhone → iCloud → watch_dir → transcription → local archive"
        echo ""
        echo "  Ways to sync iPhone recordings to iCloud Drive:"
        echo ""
        echo "  [Option A] Shortcuts automation (recommended, no manual steps):"
        echo "    1. Open Shortcuts on iPhone → Automation → +"
        echo "    2. Trigger: App → Voice Memos → Recording Finished"
        echo "    3. Turn off Ask Before Running → choose Run Immediately"
        echo "    4. Add actions: Get Latest Recording → Save File"
        echo "    5. Destination path: iCloud Drive/$ICLOUD_WATCH_SUBDIR/"
        echo ""
        echo "  [Option B] Third-party recording app (automatic sync):"
        echo "    For example Just Press Record or Voice Recorder & Audio Editor"
        echo "    Set the recording folder in the app to: iCloud Drive/$ICLOUD_WATCH_SUBDIR/"
        echo ""
        echo "  [Option C] Manual:"
        echo "    Use Files or AirDrop to place recordings into"
        echo "    iCloud Drive/$ICLOUD_WATCH_SUBDIR/"
        echo ""
        echo "  After processing, files are moved out of iCloud and no longer consume iCloud storage."
        echo "  Wait time: ${SYNC_DELAY_ICLOUD}s"
        ;;
    syncthing)
        echo "Syncthing sync mode:"
        echo "  Watch directory: $WATCH_DIR"
        echo "  Steps:"
        echo "    1. Install Syncthing on Mac: brew install syncthing"
        echo "    2. Start it: syncthing (Web UI at http://127.0.0.1:8384)"
        echo "    3. Install Syncthing on the phone (iOS: Möbius Sync / Android: Syncthing)"
        echo "    4. Configure the shared folder: phone recording folder -> $WATCH_DIR on Mac"
        echo "    5. Make sure the phone and Mac are on the same network"
        echo "  Wait time: ${SYNC_DELAY_SYNCTHING}s"
        ;;
    manual)
        echo "Manual mode:"
        echo "  Watch directory: $WATCH_DIR"
        echo "  Usage:"
        echo "    - Manually copy or move recordings to: $WATCH_DIR"
        echo "    - Or specify a file path when processing a recording"
        echo "  Wait time: ${SYNC_DELAY_MANUAL}s"
        ;;
    *)
        echo "Sync method: $SYNC_METHOD"
        echo "  Watch directory: $WATCH_DIR"
        ;;
esac
echo ""

echo "Dependencies:"
echo "  Run: python3 $SKILL_DIR/scripts/common/deps_manager.py ensure L1"
echo "  Or process an audio file — dependencies will auto-install on first use."
