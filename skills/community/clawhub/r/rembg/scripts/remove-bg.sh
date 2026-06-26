#!/bin/bash
# rembg 抠图工具
# 用法: remove-bg.sh <输入图片路径> [输出目录]

# Skill 目录
SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# 虚拟环境目录（统一放在 ~/.venv/rembg）
VENV_DIR="$HOME/.venv/rembg"

# 默认输出目录（放在用户 workspace 下）
DEFAULT_OUTPUT_DIR="$HOME/.openclaw/skills/rembg/image_output"

INPUT_FILE="$1"
OUTPUT_DIR="$2"

# 如果没有指定输出目录，使用默认目录
if [ -z "$OUTPUT_DIR" ]; then
    OUTPUT_DIR="$DEFAULT_OUTPUT_DIR/$(date +%Y-%m-%d)"
fi

# 创建输出目录（如果不存在）
mkdir -p "$OUTPUT_DIR"

if [ -z "$INPUT_FILE" ]; then
    echo "用法: remove-bg.sh <输入图片路径> [输出目录]"
    echo "示例: remove-bg.sh input.png                           # 默认保存到 image_output/今天日期/"
    echo "       remove-bg.sh input.png /path/to/output/        # 保存到指定目录"
    echo ""
    echo "Skill 目录: $SCRIPT_DIR"
    exit 1
fi

if [ ! -f "$INPUT_FILE" ]; then
    echo "错误: 输入文件不存在: $INPUT_FILE"
    exit 1
fi

# 获取输入文件名（不含路径和扩展名）
BASENAME=$(basename "$INPUT_FILE" | sed 's/\.[^.]*$//')
OUTPUT_FILE="$OUTPUT_DIR/${BASENAME}_nobg.png"

# 激活虚拟环境并运行 rembg
source "$VENV_DIR/bin/activate"
rembg i "$INPUT_FILE" "$OUTPUT_FILE"

echo "完成！输出文件: $OUTPUT_FILE"
