#!/usr/bin/env bash
# voice.sh — turn text into a WhatsApp voice note and send it.
# Pipeline: TTS -> ffmpeg (opus/ogg) -> openclaw message send --media
# The @openclaw/whatsapp plugin auto-sends any audio attachment as a real voice note (ptt:true)
# and transcodes it, but we hand it clean opus/ogg for best quality.
#
# Engines (auto-selected):
#   elevenlabs  — natural male voice in Hebrew AND English. Used when ELEVENLABS_API_KEY is set.
#   say         — macOS built-in, free, robotic. Fallback when no ElevenLabs key. (Hebrew = Carmit only.)
# Force with --engine elevenlabs|say.
#
# Usage:
#   voice.sh --target +15555550100 --text "Hi, this is your agent."
#   voice.sh --target +15555550100 --text "שלום"          # Hebrew auto-detected
#   voice.sh --target +15555550100 --text-file /path/to/note.txt
#   voice.sh --text "..." --out-only /tmp/foo.ogg                        # build file, don't send
#
# ElevenLabs config (skill .env or env vars):
#   ELEVENLABS_API_KEY   — required to use ElevenLabs
#   ELEVENLABS_VOICE_ID  — male multilingual voice id (default: Daniel onwK4e9ZLuTAKqWW03F9)
#   ELEVENLABS_MODEL     — default eleven_multilingual_v2 (best quality; supports Hebrew).
#                          Cheaper option: eleven_flash_v2_5 (~half the credits).
#
# POLICY: decide in your agent rules who may receive voice notes — do not let the agent voice arbitrary contacts.
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Load .env as DEFAULTS only — never clobber a var already set in the environment,
# so `ELEVENLABS_MODEL=... voice.sh` and exported overrides still win.
if [[ -f "$SKILL_DIR/.env" ]]; then
  while IFS='=' read -r k v; do
    [[ "$k" =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]] || continue
    [[ -n "${!k:-}" ]] && continue
    export "$k=$v"
  done < <(grep -v '^[[:space:]]*#' "$SKILL_DIR/.env")
fi

TARGET=""
TEXT=""
TEXT_FILE=""
VOICE=""
RATE="185"          # words per minute (macOS say only)
OUT_ONLY=""
DRY_RUN=""
ENGINE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)    TARGET="$2"; shift 2;;
    --text)      TEXT="$2"; shift 2;;
    --text-file) TEXT_FILE="$2"; shift 2;;
    --voice)     VOICE="$2"; shift 2;;
    --rate)      RATE="$2"; shift 2;;
    --engine)    ENGINE="$2"; shift 2;;
    --out-only)  OUT_ONLY="$2"; shift 2;;
    --dry-run)   DRY_RUN="1"; shift;;
    -h|--help)   grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 0;;
    *) echo "voice.sh: unknown arg: $1" >&2; exit 2;;
  esac
done

if [[ -n "$TEXT_FILE" ]]; then
  [[ -f "$TEXT_FILE" ]] || { echo "voice.sh: text-file not found: $TEXT_FILE" >&2; exit 2; }
  TEXT="$(cat "$TEXT_FILE")"
fi
[[ -n "$TEXT" ]] || { echo "voice.sh: --text or --text-file required" >&2; exit 2; }
[[ -n "$TARGET" || -n "$OUT_ONLY" ]] || { echo "voice.sh: --target required (or use --out-only)" >&2; exit 2; }
command -v ffmpeg >/dev/null || { echo "voice.sh: ffmpeg not found (brew install ffmpeg)" >&2; exit 1; }

# Pick engine: explicit flag > ElevenLabs if key present > macOS say.
if [[ -z "$ENGINE" ]]; then
  if [[ -n "${ELEVENLABS_API_KEY:-}" ]]; then ENGINE="elevenlabs"; else ENGINE="say"; fi
fi

TMP="$(mktemp -d "${TMPDIR:-/tmp}/voice-note-XXXXXX")"
trap 'rm -rf "$TMP"' EXIT
OGG="${OUT_ONLY:-$TMP/voice.ogg}"

if [[ "$ENGINE" == "elevenlabs" ]]; then
  [[ -n "${ELEVENLABS_API_KEY:-}" ]] || { echo "voice.sh: ELEVENLABS_API_KEY not set (add to $SKILL_DIR/.env)" >&2; exit 1; }
  VOICE_ID="${VOICE:-${ELEVENLABS_VOICE_ID:-onwK4e9ZLuTAKqWW03F9}}"   # default: Daniel (male)
  # Auto-pick model by language: Hebrew needs eleven_v3 (only model that supports it);
  # everything else uses the stable, great-sounding multilingual_v2. Caller can override
  # via ELEVENLABS_MODEL.
  if [[ -n "${ELEVENLABS_MODEL:-}" ]]; then
    MODEL="$ELEVENLABS_MODEL"
  elif printf '%s' "$TEXT" | LC_ALL=en_US.UTF-8 grep -qP '[\x{0590}-\x{05FF}]' 2>/dev/null \
       || printf '%s' "$TEXT" | perl -CSD -ne 'exit(/\p{Hebrew}/ ? 0 : 1)'; then
    MODEL="eleven_v3"
  else
    MODEL="eleven_multilingual_v2"
  fi
  MP3="$TMP/voice.mp3"
  # Build JSON body safely (text may contain quotes / Hebrew / newlines).
  BODY="$(MODEL="$MODEL" TEXT="$TEXT" python3 -c 'import json,os;print(json.dumps({"text":os.environ["TEXT"],"model_id":os.environ["MODEL"],"voice_settings":{"stability":0.5,"similarity_boost":0.8}}))')"
  code=$(curl -sS -o "$MP3" -w "%{http_code}" \
    "https://api.elevenlabs.io/v1/text-to-speech/${VOICE_ID}" \
    -H "xi-api-key: ${ELEVENLABS_API_KEY}" -H "Content-Type: application/json" \
    --data "$BODY")
  if [[ "$code" != "200" ]]; then
    echo "voice.sh: ElevenLabs HTTP $code" >&2; head -c 400 "$MP3" >&2; echo >&2; exit 1
  fi
  ffmpeg -nostdin -y -i "$MP3" -ac 1 -ar 48000 -c:a libopus -b:a 32k "$OGG" >/dev/null 2>&1
  USED="elevenlabs:$VOICE_ID:$MODEL"
else
  command -v say >/dev/null || { echo "voice.sh: macOS 'say' not found" >&2; exit 1; }
  # macOS voices: English -> Reed (male). Hebrew -> Carmit (female; no male Hebrew on macOS).
  VOICE_EN="${VOICE_EN:-Reed (English (US))}"
  VOICE_HE="${VOICE_HE:-Carmit}"
  SAYVOICE="$VOICE"
  if [[ -z "$SAYVOICE" ]]; then
    if printf '%s' "$TEXT" | LC_ALL=en_US.UTF-8 grep -qP '[\x{0590}-\x{05FF}]' 2>/dev/null \
       || printf '%s' "$TEXT" | perl -CSD -ne 'exit(/\p{Hebrew}/ ? 0 : 1)'; then
      SAYVOICE="$VOICE_HE"
    else
      SAYVOICE="$VOICE_EN"
    fi
  fi
  AIFF="$TMP/voice.aiff"
  say -v "$SAYVOICE" -r "$RATE" -o "$AIFF" "$TEXT"
  ffmpeg -nostdin -y -i "$AIFF" -ac 1 -ar 48000 -c:a libopus -b:a 32k "$OGG" >/dev/null 2>&1
  USED="say:$SAYVOICE"
fi

SECS="$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "$OGG" 2>/dev/null || echo "?")"
echo "voice.sh: built $OGG (engine=$USED, ${SECS}s)"

if [[ -n "$OUT_ONLY" ]]; then
  exit 0
fi

ARGS=(message send --channel whatsapp --target "$TARGET" --media "$OGG")
[[ -n "$DRY_RUN" ]] && ARGS+=(--dry-run)
openclaw "${ARGS[@]}"
