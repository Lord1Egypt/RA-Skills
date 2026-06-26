#!/bin/bash
# quick-generate.sh - one-click image generation
# Usage: bash quick-generate.sh "positive prompt" "negative prompt" [workflow] [output_dir]

set -euo pipefail

POSITIVE="${1:?Usage: bash quick-generate.sh \"positive\" \"negative\" [workflow] [output_dir]}"
NEGATIVE="${2:-lowres, bad anatomy, bad hands, blurry, worst quality, watermark}"
WORKFLOW="${3:-sdxl_basic.json}"
OUTPUT_DIR="${4:-/home/node/ai-outputs}"
WORKDIR="/home/node/.openclaw/workspace"
WORKFLOW_PATH="$WORKDIR/workflows/$WORKFLOW"

if [ ! -f "$WORKFLOW_PATH" ]; then
  echo "ERROR: workflow not found: $WORKFLOW_PATH"
  exit 1
fi

echo "[1/5] Checking ComfyUI..."
COMFY_CHECK=$(curl -s --connect-timeout 5 http://host.docker.internal:8188/system_stats 2>/dev/null)
if [ -z "$COMFY_CHECK" ]; then
  echo "ERROR: ComfyUI is not running"
  exit 1
fi
echo "OK: ComfyUI online"

mkdir -p "$OUTPUT_DIR"
SEED=$((RANDOM * RANDOM))
START_TS=$(date +%s)
TMP_WORKFLOW=$(mktemp /tmp/quick-workflow.XXXXXX.json)
trap 'rm -f "$TMP_WORKFLOW"' EXIT

echo "[2/5] Building workflow with prompt+seed..."
python3 - "$WORKFLOW_PATH" "$TMP_WORKFLOW" "$POSITIVE" "$NEGATIVE" "$SEED" <<'PY'
import json, sys
src, dst, positive, negative, seed = sys.argv[1:6]
seed = int(seed)
wf = json.load(open(src, 'r', encoding='utf-8'))

# Preferred node ids for current templates
if isinstance(wf.get('6'), dict):
    wf['6'].setdefault('inputs', {})['text'] = positive
if isinstance(wf.get('7'), dict):
    wf['7'].setdefault('inputs', {})['text'] = negative
if isinstance(wf.get('3'), dict):
    wf['3'].setdefault('inputs', {})['seed'] = seed

# Fallback by class_type to keep script robust
pos_done = neg_done = seed_done = False
for node in wf.values():
    if not isinstance(node, dict):
        continue
    c = node.get('class_type')
    inputs = node.get('inputs')
    if not isinstance(inputs, dict):
        continue
    if c == 'KSampler':
        inputs['seed'] = seed
        seed_done = True
    elif c == 'CLIPTextEncode' and not pos_done:
        inputs['text'] = positive
        pos_done = True
    elif c == 'CLIPTextEncode' and pos_done and not neg_done:
        inputs['text'] = negative
        neg_done = True

with open(dst, 'w', encoding='utf-8') as f:
    json.dump(wf, f, ensure_ascii=False)
PY

echo "[3/5] Generating..."
echo "  Prompt: ${POSITIVE:0:80}..."
echo "  Workflow: $WORKFLOW"
echo "  Seed: $SEED"
python3 "$WORKDIR/tools/comfyui-client.py" wait --workflow "$TMP_WORKFLOW" --output-dir "$OUTPUT_DIR"

LATEST_FILE=$(find "$OUTPUT_DIR" -maxdepth 1 -name '*.png' -type f -newermt "@$START_TS" 2>/dev/null | sort | tail -1)
if [ -z "$LATEST_FILE" ]; then
  echo "ERROR: no new generated image found for this run"
  exit 1
fi

FILE_SIZE=$(stat -f%z "$LATEST_FILE" 2>/dev/null || stat -c%s "$LATEST_FILE" 2>/dev/null)
if [ "$FILE_SIZE" -lt 100000 ]; then
  echo "WARN: file too small (${FILE_SIZE} bytes), possible black image"
  exit 1
fi

echo "SUCCESS"
echo "FILE=$LATEST_FILE"
echo "SIZE_KB=$((FILE_SIZE / 1024))"
echo "SEED=$SEED"
