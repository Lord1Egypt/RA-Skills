#!/bin/bash
# paint-dispatch.sh — 接收 JSON 输入，调用 ComfyUI 出图
# 用法：echo "JSON" | bash paint-dispatch.sh
# 或：bash paint-dispatch.sh "JSON字符串"

set -euo pipefail

# 读取 JSON 输入（从参数或 stdin）
if [ -n "${1:-}" ]; then
    JSON_INPUT="$1"
else
    JSON_INPUT=$(cat)
fi

if [ -z "${JSON_INPUT:-}" ]; then
    echo "ERROR: 没有收到 JSON 输入"
    exit 1
fi

# 解析 JSON
POSITIVE=$(echo "$JSON_INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('positive',''))")
NEGATIVE=$(echo "$JSON_INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('negative','lowres, bad anatomy, bad hands, blurry, worst quality, watermark, signature, text'))")
WORKFLOW=$(echo "$JSON_INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('workflow','sdxl_basic.json'))")
CHECKPOINT=$(echo "$JSON_INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('checkpoint',''))")
SEED=$(echo "$JSON_INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('seed',-1))")

OUTPUT_DIR="/home/node/ai-outputs"
WORKDIR="/home/node/.openclaw/workspace"

# workflow 白名单
case "$WORKFLOW" in
  sdxl_basic.json|sdxl_hires.json) ;;
  *)
    echo "WARNING: workflow=$WORKFLOW 非法，回退到 sdxl_basic.json"
    WORKFLOW="sdxl_basic.json"
    ;;
esac

if [ -z "$POSITIVE" ]; then
    echo "ERROR: positive 为空"
    exit 1
fi

# 如果 seed 是 -1，生成随机值
if [ "$SEED" = "-1" ]; then
    SEED=$((RANDOM * RANDOM))
fi

# Step 1: 检查 ComfyUI
if ! python3 "$WORKDIR/tools/comfyui-client.py" health >/tmp/comfy_health.json 2>/tmp/comfy_health.err; then
    echo "ERROR: ComfyUI 未运行或不可达"
    cat /tmp/comfy_health.err || true
    exit 1
fi

# Step 1.5: 校验 checkpoint 是否可用，不可用则回退到 ComfyUI 当前可用的第一个模型
if [ -n "$CHECKPOINT" ]; then
    AVAILABLE_CKPT=$(
        curl -s --connect-timeout 5 http://host.docker.internal:8188/object_info/CheckpointLoaderSimple \
        | python3 -c "import json,sys; d=json.load(sys.stdin); arr=d.get('CheckpointLoaderSimple',{}).get('input',{}).get('required',{}).get('ckpt_name',[[]])[0]; print(','.join(arr) if isinstance(arr,list) else '')" \
        2>/dev/null || true
    )
    if [ -n "$AVAILABLE_CKPT" ]; then
        export CHECKPOINT AVAILABLE_CKPT
        CKPT_OK=$(
            python3 - <<'PY'
import os
ckpt = os.environ.get("CHECKPOINT", "")
avail = [x for x in os.environ.get("AVAILABLE_CKPT", "").split(",") if x]
print("1" if ckpt in avail else "0")
PY
        )
        if [ "$CKPT_OK" != "1" ]; then
            FALLBACK_CKPT=$(echo "$AVAILABLE_CKPT" | cut -d',' -f1)
            echo "WARNING: checkpoint '$CHECKPOINT' 不可用，回退为 '$FALLBACK_CKPT'"
            CHECKPOINT="$FALLBACK_CKPT"
        fi
    fi
fi

# Step 2: 创建输出目录与临时 workflow
mkdir -p "$OUTPUT_DIR"
TEMPLATE_WORKFLOW="$WORKDIR/workflows/$WORKFLOW"
if [ ! -f "$TEMPLATE_WORKFLOW" ]; then
    echo "ERROR: workflow 不存在: $TEMPLATE_WORKFLOW"
    exit 1
fi
TMP_WORKFLOW="/tmp/paint-workflow-$$.json"
export TEMPLATE_WORKFLOW TMP_WORKFLOW POSITIVE NEGATIVE CHECKPOINT SEED
python3 - <<'PY'
import json, os
src=os.environ['TEMPLATE_WORKFLOW']
out=os.environ['TMP_WORKFLOW']
pos=os.environ['POSITIVE']
neg=os.environ['NEGATIVE']
ckpt=os.environ.get('CHECKPOINT','').strip()
seed=int(os.environ['SEED'])

wf=json.load(open(src, 'r', encoding='utf-8'))

# 按 KSampler 链路精确替换正负提示词
for node in wf.values():
    if isinstance(node, dict) and node.get('class_type') == 'KSampler':
        ins=node.get('inputs', {})
        ins['seed']=seed
        pos_ref=ins.get('positive')
        neg_ref=ins.get('negative')
        if isinstance(pos_ref, list) and pos_ref:
            pos_id=str(pos_ref[0])
            if pos_id in wf and isinstance(wf[pos_id], dict):
                wf[pos_id].setdefault('inputs', {})['text']=pos
        if isinstance(neg_ref, list) and neg_ref:
            neg_id=str(neg_ref[0])
            if neg_id in wf and isinstance(wf[neg_id], dict):
                wf[neg_id].setdefault('inputs', {})['text']=neg

# checkpoint 覆盖
if ckpt:
    for node in wf.values():
        if isinstance(node, dict) and node.get('class_type') == 'CheckpointLoaderSimple':
            node.setdefault('inputs', {})['ckpt_name']=ckpt

with open(out, 'w', encoding='utf-8') as f:
    json.dump(wf, f, ensure_ascii=False)
PY

# Step 3: 执行出图
echo "开始生成..."
echo "Prompt: ${POSITIVE:0:80}..."
echo "Workflow: $WORKFLOW"
echo "Checkpoint: ${CHECKPOINT:-<template>}"
echo "Seed: $SEED"

set +e
RESULT=$(python3 "$WORKDIR/tools/comfyui-client.py" wait \
  --workflow "$TMP_WORKFLOW" \
  --output-dir "$OUTPUT_DIR" 2>&1)
RET=$?
set -e

echo "$RESULT"
rm -f "$TMP_WORKFLOW"

if [ $RET -ne 0 ]; then
    echo "ERROR: comfyui-client 执行失败"
    exit $RET
fi

# Step 4: 读取输出文件（以本次返回为准）
FILE_PATH=$(echo "$RESULT" | python3 -c "import json,sys; raw=sys.stdin.read().strip(); obj=json.loads(raw) if raw else {}; files=obj.get('output_files',[]); print(files[0] if files else '')")
if [ -z "$FILE_PATH" ] || [ ! -f "$FILE_PATH" ]; then
    echo "ERROR: 未找到本次生成图片"
    exit 1
fi

FILE_SIZE=$(stat -c%s "$FILE_PATH" 2>/dev/null || stat -f%z "$FILE_PATH" 2>/dev/null)
if [ "$FILE_SIZE" -lt 100000 ]; then
    echo "WARNING: 文件偏小(${FILE_SIZE}bytes)，可能是黑图"
fi

echo "SUCCESS"
echo "FILE: $FILE_PATH"
echo "SIZE: $((FILE_SIZE / 1024))KB"
echo "SEED: $SEED"
