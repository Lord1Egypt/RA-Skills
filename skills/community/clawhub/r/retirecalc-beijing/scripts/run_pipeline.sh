#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <input-file> [work-dir]"
  exit 1
fi

INPUT="$1"
WORK_DIR="${2:-./tmp}"
mkdir -p "$WORK_DIR"

INGEST_OUT="$WORK_DIR/ingested.json"
CALC_OUT="$WORK_DIR/result.json"
CONFIRM_OUT="$WORK_DIR/confirmation_form.md"

python3 scripts/ingest_user_data.py --input "$INPUT" --output "$INGEST_OUT"
python3 scripts/export_confirmation_form.py --input "$INGEST_OUT" --output "$CONFIRM_OUT"
python3 scripts/calc_pension_beijing.py --input "$INGEST_OUT" > "$CALC_OUT"

echo "Done"
echo "ingest: $INGEST_OUT"
echo "confirm: $CONFIRM_OUT"
echo "result: $CALC_OUT"
