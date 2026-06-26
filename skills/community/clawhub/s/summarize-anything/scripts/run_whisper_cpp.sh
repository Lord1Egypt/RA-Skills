#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: run_whisper_cpp.sh <input-file> <output-prefix> [language] [model-name]" >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
INPUT="$1"
OUTPUT_PREFIX="$2"
LANGUAGE="${3:-zh}"
MODEL_NAME="${4:-small}"

"${SCRIPT_DIR}/maintain_runtime.sh" >/dev/null 2>&1 || true

WHISPER_BIN="$("${SCRIPT_DIR}/ensure_whisper_cpp.sh")"
MODEL_PATH="$("${SCRIPT_DIR}/ensure_whisper_model.sh" "${MODEL_NAME}")"

mkdir -p "$(dirname "${OUTPUT_PREFIX}")"

WORK_AUDIO="${SKILL_DIR}/runtime/work/$(basename "${INPUT%.*}").wav"
AUDIO_INPUT="${INPUT}"
CLEANUP_AUDIO=0
case "${INPUT##*.}" in
  wav|WAV|mp3|MP3|flac|FLAC|ogg|OGG)
    ;;
  *)
    AUDIO_INPUT="$("${SCRIPT_DIR}/extract_audio.sh" "${INPUT}" "${WORK_AUDIO}")"
    CLEANUP_AUDIO=1
    ;;
esac

cleanup() {
  if [[ "${CLEANUP_AUDIO}" -eq 1 && -f "${AUDIO_INPUT}" ]]; then
    rm -f "${AUDIO_INPUT}"
  fi
}

trap cleanup EXIT

"${WHISPER_BIN}" \
  -m "${MODEL_PATH}" \
  -f "${AUDIO_INPUT}" \
  -l "${LANGUAGE}" \
  -otxt -osrt -oj \
  -of "${OUTPUT_PREFIX}" \
  -np

"${SCRIPT_DIR}/maintain_runtime.sh" >/dev/null 2>&1 || true

echo "${OUTPUT_PREFIX}.txt"
