#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORKSPACE="${OPENCLAW_WORKSPACE:-$(pwd)}"
TMP_DIR="$WORKSPACE/tmp"
STATE_DIR="$WORKSPACE/skills/text-to-voice-local/state"
VOICE_WRAPPER="$SKILL_DIR/scripts/voice_reply_latest.sh"
DEFAULT_TEXT_OUT="$TMP_DIR/text-to-voice-input.txt"
DEFAULT_VOICE="ru-RU-DmitryNeural"
DEFAULT_MAX_DIRECT_CHARS="280"
STATE_FILE="$STATE_DIR/text-to-voice.json"

mkdir -p "$TMP_DIR" "$STATE_DIR"

init_state() {
  [ -f "$STATE_FILE" ] || cat > "$STATE_FILE" <<EOF
{
  "default_voice": "$DEFAULT_VOICE",
  "max_direct_chars": $DEFAULT_MAX_DIRECT_CHARS,
  "canonical_input": "$DEFAULT_TEXT_OUT",
  "canonical_output": "$TMP_DIR/voice-mode-latest.mp3"
}
EOF
}

read_state_value() {
  key="$1"
  python3 - "$STATE_FILE" "$key" <<'PY'
import json, sys
p, k = sys.argv[1], sys.argv[2]
with open(p, 'r', encoding='utf-8') as f:
    data = json.load(f)
print(data.get(k, ''))
PY
}

init_state

check_dependencies() {
  missing=0

  if command -v node >/dev/null 2>&1; then
    node_status="ok"
  else
    node_status="missing"
    missing=1
  fi

  if command -v ffmpeg >/dev/null 2>&1; then
    ffmpeg_status="ok"
  else
    ffmpeg_status="missing"
    missing=1
  fi

  if node -e "require('node-edge-tts')" >/dev/null 2>&1; then
    edge_tts_status="ok"
  elif [ -d /usr/lib/node_modules/openclaw/node_modules/node-edge-tts ]; then
    edge_tts_status="ok (openclaw bundled fallback)"
  else
    edge_tts_status="missing"
    missing=1
  fi

  printf 'Dependency check:\n'
  printf -- '- node: %s\n' "$node_status"
  printf -- '- ffmpeg: %s\n' "$ffmpeg_status"
  printf -- '- node-edge-tts: %s\n' "$edge_tts_status"

  if [ "$missing" -ne 0 ]; then
    printf '\nSuggested install commands:\n'
    [ "$node_status" = "missing" ] && printf -- '- install node via your system package manager or nvm\n'
    [ "$ffmpeg_status" = "missing" ] && printf -- '- sudo apt install ffmpeg\n'
    if [ "$edge_tts_status" = "missing" ]; then
      printf -- '- npm i -g node-edge-tts\n'
    fi
  fi

  return "$missing"
}

ensure_dependencies() {
  if ! check_dependencies; then
    exit 2
  fi
}

progress_bar() {
  pct="$1"
  label="$2"
  filled=$((pct / 5))
  if [ "$filled" -gt 20 ]; then
    filled=20
  fi
  empty=$((20 - filled))
  bar=""
  i=0
  while [ "$i" -lt "$filled" ]; do bar="${bar}▓"; i=$((i + 1)); done
  i=0
  while [ "$i" -lt "$empty" ]; do bar="${bar}░"; i=$((i + 1)); done
  printf '🎙️ Озвучка текста: %s %s%% · %s\n' "$bar" "$pct" "$label"
}

usage() {
  cat >&2 <<'EOF'
Usage:
  text_to_voice.sh text [text-file]
  text_to_voice.sh voice [text-file] [voice] [max_direct_chars]
  text_to_voice.sh voice-progress [text-file] [voice] [max_direct_chars]
  text_to_voice.sh status
  text_to_voice.sh voices
EOF
  exit 1
}

cmd="${1:-}"
case "$cmd" in
  text)
    mkdir -p "$TMP_DIR"
    printf '%s\n' "${2:-$DEFAULT_TEXT_OUT}"
    ;;
  voice)
    text_file="${2:-$DEFAULT_TEXT_OUT}"
    voice="${3:-$(read_state_value default_voice)}"
    max_direct_chars="${4:-$(read_state_value max_direct_chars)}"
    [ -f "$text_file" ] || { echo "Input text file not found: $text_file" >&2; exit 2; }
    ensure_dependencies
    exec "$VOICE_WRAPPER" "$text_file" "$voice" "$max_direct_chars"
    ;;
  voice-progress)
    text_file="${2:-$DEFAULT_TEXT_OUT}"
    voice="${3:-$(read_state_value default_voice)}"
    max_direct_chars="${4:-$(read_state_value max_direct_chars)}"
    [ -f "$text_file" ] || { echo "Input text file not found: $text_file" >&2; exit 2; }
    ensure_dependencies
    progress_bar 2 "Старт"; sleep 0.08
    progress_bar 10 "Читаю текст"; sleep 0.08
    progress_bar 18 "Проверяю voice settings"; sleep 0.08
    progress_bar 30 "Запускаю озвучку"; sleep 0.08
    progress_bar 48 "Генерирую чанки"; sleep 0.08
    progress_bar 68 "Собираю аудио"; sleep 0.08
    progress_bar 86 "Пишу canonical output"; sleep 0.08
    "$VOICE_WRAPPER" "$text_file" "$voice" "$max_direct_chars" >/dev/null
    progress_bar 100 "Готово"
    printf '%s\n' "$TMP_DIR/voice-mode-latest.mp3"
    ;;
  status)
    cat "$STATE_FILE"
    printf '\n'
    check_dependencies || true
    ;;
  voices)
    cat <<'EOF'
Recommended voices:
- ru-RU-DmitryNeural
- ru-RU-SvetlanaNeural
- en-US-AriaNeural
- en-US-GuyNeural
- el-GR-AthinaNeural
- el-GR-NestorasNeural
EOF
    ;;
  *) usage ;;
esac
