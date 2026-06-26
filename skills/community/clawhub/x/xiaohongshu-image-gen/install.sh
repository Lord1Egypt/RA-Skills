#!/bin/bash

# 小红书图片生成技能安装脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🔥 小红书图片生成技能安装中..."
echo ""

# 检查 Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到 python3"
    exit 1
fi

echo "✅ 找到 python3: $(python3 --version)"

# 创建 source 目录
mkdir -p "$SCRIPT_DIR/source"

# 检查主脚本
if [ ! -f "$SCRIPT_DIR/source/xiaohongshu_image_gen.py" ]; then
    echo "❌ 错误：缺少 source/xiaiaohongshu_image_gen.py"
    exit 1
fi

echo ""
echo "✅ 小红书图片生成技能安装完成！"
echo ""
echo "📖 使用方法："
echo "  xiaohongshu-image-gen --prompt '客厅现代简约风格装修设计' --style '家装'"
echo "  xiaohongshu-image-gen --prompt '精致早餐摆盘' --style '美食'"
echo "  xiaohongshu-image-gen --prompt '春季穿搭搭配' --style '穿搭'"
