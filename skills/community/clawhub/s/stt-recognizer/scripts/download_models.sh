#!/bin/bash
#==============================================================================
# Whisper Model Downloader - stt-recognizer 技能专用
# 自动下载 Whisper 模型到统一缓存位置
#==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# 模型统一存放在缓存位置，按技能命名
# 格式：~/.cache/huggingface/modules/<技能名>/<模型大小>/
CACHE_MODELS_DIR="$HOME/.cache/huggingface/modules/stt-recognizer"

# Model size guide:
# tiny=39M, base=74M, small=244M, medium=769M, large=1550M

MODEL_SIZE="${1:-small}"

# 验证模型大小
VALID_SIZES="tiny base small medium large"
if [[ ! " $VALID_SIZES " =~ " $MODEL_SIZE " ]]; then
    echo "错误: 无效的模型大小 '$MODEL_SIZE'"
    echo "可用大小: $VALID_SIZES"
    exit 1
fi

# 模型输出目录
OUTPUT_DIR="${CACHE_MODELS_DIR}/${MODEL_SIZE}"

echo "=========================================="
echo " Whisper Model Downloader"
echo "=========================================="
echo ""
echo "技能目录: ${SKILL_DIR}"
echo "缓存目录: ${CACHE_MODELS_DIR}"
echo "模型大小: ${MODEL_SIZE}"
echo "输出目录: ${OUTPUT_DIR}"
echo ""

# 创建目录
mkdir -p "${OUTPUT_DIR}"

# Pass variables via environment to avoid Python code injection
export MODEL_SIZE
export OUTPUT_DIR

# Use Python to download faster-whisper models
python3 - << 'PYEOF'
import os
import sys
from faster_whisper import download_model

model_size = os.environ.get('MODEL_SIZE', 'small')
output_dir = os.environ.get('OUTPUT_DIR', '.')

print(f'Downloading faster-whisper model: {model_size}...')
try:
    path = download_model(model_size, output_dir=output_dir)
    print(f'Model saved to: {path}')
except Exception as e:
    print(f'Error: {e}', file=sys.stderr)
    sys.exit(1)
PYEOF

echo ""
echo "=========================================="
echo " 模型下载完成！"
echo "=========================================="
echo ""
echo "模型位置: ${OUTPUT_DIR}"
ls -lh "${OUTPUT_DIR}" 2>/dev/null || echo "  (目录为空)"
echo ""
echo "可用模型大小: tiny, base, small, medium, large"
echo "下载其他模型: bash scripts/download_models.sh small"
echo ""
echo "提示: 所有 stt-recognizer 模型统一存放在:"
echo "  ~/.cache/huggingface/modules/stt-recognizer/"
