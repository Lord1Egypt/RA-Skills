#!/bin/bash
#
# SGLang Benchmark Runner
#
# Usage:
#   MODEL_PATH=/data/models/DeepSeek-R1 bash bench.sh 2>&1 | tee bench.log
#
# Override defaults with env vars:
#   ISL=2048 OSL=512 PORT=8000 CONCURRENCY="32 64 128" OUTPUT_DIR=/sgl-workspace MODEL_PATH=... bash bench.sh
#

set -euo pipefail

export PYTHONPATH=/sgl-workspace/sglang/python:${PYTHONPATH:-}

: "${MODEL_PATH:?Error: MODEL_PATH must be set}"

ISL="${ISL:-4096}"
OSL="${OSL:-1024}"
RATIO="${RATIO:-1.0}"
PORT="${PORT:-30000}"
CONCURRENCY="${CONCURRENCY:-64 128}"
OUTPUT_DIR="${OUTPUT_DIR:-/sgl-workspace}"
JSONL_DIR="${OUTPUT_DIR}/jsonl_dir"

mkdir -p "$JSONL_DIR"

echo "======================================================================"
echo "SGLang Benchmark"
echo "  Model:       ${MODEL_PATH}"
echo "  ISL:         ${ISL}"
echo "  OSL:         ${OSL}"
echo "  Ratio:       ${RATIO}"
echo "  Concurrency: ${CONCURRENCY}"
echo "  Output dir:  ${OUTPUT_DIR}"
echo "  Started:     $(date -Iseconds)"
echo "======================================================================"

for CON in $CONCURRENCY; do
  PROMPTS=$((CON * 2))
  OUT="${JSONL_DIR}/bench_ISL${ISL}_OSL${OSL}_CON${CON}.jsonl"

  echo ""
  echo "[$(date -Iseconds)] ISL=${ISL} OSL=${OSL} CON=${CON} PROMPTS=${PROMPTS} -> ${OUT}"

  python3 -m sglang.bench_serving \
    --dataset-name random \
    --model "$MODEL_PATH" \
    --random-input-len "$ISL" \
    --random-output-len "$OSL" \
    --num-prompt "$PROMPTS" \
    --random-range-ratio "$RATIO" \
    --max-concurrency "$CON" \
    --host 0.0.0.0 \
    --port "$PORT" \
    --output-file "$OUT"
done

echo ""
echo "Done at $(date -Iseconds). JSONL: ${JSONL_DIR}"
