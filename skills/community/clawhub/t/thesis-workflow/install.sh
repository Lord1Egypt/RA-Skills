#!/bin/bash
# MBA Thesis Workflow - 安装脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$SCRIPT_DIR"

echo "=== MBA Thesis Workflow 安装向导 ==="
echo ""

# 检测是否已存在 config.env
if [ -f "$SKILL_DIR/config.env" ]; then
    echo "✅ 检测到已存在 config.env，将跳过配置（如需重新配置请先删除）"
else
    echo "📝 首次安装，需要填写配置..."
    echo ""

    # 读取模板
    WORKSPACE_ROOT=$(grep "^WORKSPACE_ROOT=" "$SKILL_DIR/config.template" | cut -d= -f2)
    USER_EMAIL=""
    SENDER_EMAIL=""
    AUTHOR_NAME=""

    read -p "工作区根目录 [$WORKSPACE_ROOT]: " input
    WORKSPACE_ROOT=${input:-$WORKSPACE_ROOT}

    read -p "用户邮箱（接收论文终稿）: " USER_EMAIL
    while [ -z "$USER_EMAIL" ]; do
        echo "⚠️ 邮箱不能为空"
        read -p "用户邮箱: " USER_EMAIL
    done

    read -p "发件邮箱（QQ邮箱，用于发送邮件）: " SENDER_EMAIL
    while [ -z "$SENDER_EMAIL" ]; do
        echo "⚠️ 发件邮箱不能为空"
        read -p "发件邮箱: " SENDER_EMAIL
    done

    read -p "作者姓名: " AUTHOR_NAME

    # 写入 config.env
    cat > "$SKILL_DIR/config.env" << EOF
# MBA Thesis Workflow 配置（自动生成）
WORKSPACE_ROOT=$WORKSPACE_ROOT
USER_EMAIL=$USER_EMAIL
SENDER_EMAIL=$SENDER_EMAIL
AUTHOR_NAME=$AUTHOR_NAME
EOF

    echo ""
    echo "✅ 配置已保存到 $SKILL_DIR/config.env"
fi

# 检测依赖
echo ""
echo "🔍 检测依赖..."

# Python
if command -v python3 &>/dev/null; then
    PY_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo "✅ Python: $PY_VERSION"
else
    echo "❌ Python3 未安装"
    exit 1
fi

# python-docx
if python3 -c "import docx" 2>/dev/null; then
    echo "✅ python-docx 已安装"
else
    echo "⚠️ python-docx 未安装，尝试安装..."
    python3 -m pip install --user python-docx
fi

# OpenClaw
if command -v openclaw &>/dev/null; then
    echo "✅ OpenClaw 已安装"
else
    echo "⚠️ OpenClaw 未安装，版本H将回退到OpenClaw模式"
fi

# Hermes（可选）
if command -v hermes &>/dev/null; then
    HERMES_VERSION=$(hermes --version 2>&1 | head -1)
    echo "✅ Hermes 已安装: $HERMES_VERSION"
    HERMES_AVAILABLE=1
else
    echo "⚠️ Hermes 未安装，版本H将回退到OpenClaw模式"
    HERMES_AVAILABLE=0
fi

# 检查依赖 skill
echo ""
echo "🔍 检查依赖 Skill..."
if [ -d "$HOME/.openclaw/workspace/skills/multi-search-engine" ]; then
    echo "✅ multi-search-engine 已安装"
else
    echo "⚠️ multi-search-engine 未安装，建议安装以支持行业数据搜索"
fi

if [ -d "$HOME/.openclaw/workspace/skills/academic-research" ]; then
    echo "✅ academic-research 已安装"
else
    echo "⚠️ academic-research 未安装，建议安装以支持学术文献搜索"
fi

echo ""
echo "=== 安装完成 ==="
echo ""
echo "下一步："
echo "1. 将 config.env 中的邮箱信息填写完整（如尚未填写）"
echo "2. 使用 openclaw skills check 查看已安装的 skill"
echo "3. 开始使用：与 AI 对话启动 MBA 论文写作流程"
echo ""