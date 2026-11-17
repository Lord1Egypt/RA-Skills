#!/usr/bin/env bash
# ==============================================================
# word-formatter v1.0.0「黑灰白」— 一键安装/更新脚本
# 用法：
#   首次安装   bash install.sh
#   更新版本   bash install.sh update
# ==============================================================
set -e

REPO_URL="git@gitee.com:jeffwooo/word-formatter.git"
TARGET_DIR="${HOME}/.workbuddy/skills/word-formatter"

if [ "$1" = "update" ]; then
    echo "🔄 正在更新 word-formatter 技能..."
    cd "$TARGET_DIR"
    git pull
    # 如有依赖更新
    if [ -f requirements.txt ]; then
        .venv/bin/pip install -r requirements.txt 2>/dev/null || true
    fi
    echo "✅ 更新完成！版本：$(git describe --tags --always 2>/dev/null || echo 'latest')"
    exit 0
fi

# ——— 首次安装 ———
echo "📦 正在安装 word-formatter v1.0.0「黑灰白」..."

# 检测是否已安装
if [ -d "$TARGET_DIR/.git" ]; then
    echo "⚠️  技能已安装。如需更新请执行: bash install.sh update"
    exit 1
fi

# 克隆仓库
mkdir -p "$(dirname "$TARGET_DIR")"
git clone "$REPO_URL" "$TARGET_DIR"
cd "$TARGET_DIR"

# 创建 Python 虚拟环境
echo "🐍 创建 Python 虚拟环境..."
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install python-docx matplotlib pillow

echo ""
echo "✅ 安装完成！"
echo ""
echo "📖 使用方法："
echo "  排版文档：  .venv/bin/python scripts/format_docx.py <输入.docx> configs/<配置.json> -o <输出.docx>"
echo "  合规校验：  .venv/bin/python scripts/validate_docx.py <输出.docx> configs/<配置.json>"
echo ""
echo "🔄 更新技能：  bash $(basename "$0") update"
echo ""
