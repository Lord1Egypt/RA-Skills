#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 6 ]; then
  echo "Usage: $0 <input> <output_dir> <source_lang> <target_lang> <piper_model> <translation_file> [extra args...]" >&2
  exit 1
fi

INPUT="$1"
OUTPUT_DIR="$2"
SOURCE_LANG="$3"
TARGET_LANG="$4"
PIPER_MODEL="$5"
TRANSLATION_FILE="$6"
shift 6

python3 "$(dirname "$0")/run_voice_translate.py" \
  --input "$INPUT" \
  --output-dir "$OUTPUT_DIR" \
  --source-lang "$SOURCE_LANG" \
  --target-lang "$TARGET_LANG" \
  --translation-backend llm \
  --translation-file "$TRANSLATION_FILE" \
  --piper-model "$PIPER_MODEL" \
  "$@"
