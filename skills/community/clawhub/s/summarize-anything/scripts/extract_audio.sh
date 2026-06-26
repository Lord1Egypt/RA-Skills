#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: extract_audio.sh <input-media> <output-audio>" >&2
  exit 1
fi

INPUT="$1"
OUTPUT="$2"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FFMPEG_BIN="$(bash "${SCRIPT_DIR}/ensure_ffmpeg.sh")"

mkdir -p "$(dirname "${OUTPUT}")"
"${FFMPEG_BIN}" -y -i "${INPUT}" -vn -ac 1 -ar 16000 "${OUTPUT}" >/dev/null 2>&1
echo "${OUTPUT}"
