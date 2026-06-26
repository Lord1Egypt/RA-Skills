#!/bin/bash
set -e

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_DIR="$HOME/.config/skill-c-fetch-minutes"
ENV_FILE="$CONFIG_DIR/.env"

echo "🚀 设置 Skill-C (fetch_minutes)..."
echo ""

mkdir -p "$CONFIG_DIR"

echo "📦 安装 Python 依赖..."
pip install -r "$SKILL_DIR/requirements.txt" --break-system-packages -q
echo "✅ Python 依赖安装完成"

if [ ! -f "$ENV_FILE" ]; then
    cp "$SKILL_DIR/env-example.txt" "$ENV_FILE"
    chmod 600 "$ENV_FILE"
    echo ""
    echo "📝 已创建配置文件：$ENV_FILE"
    echo "请编辑该文件，至少填入："
    echo "  - GITEA_BASE_URL"
    echo "  - GITEA_TOKEN_BOT"
    echo "  - AIFUSION_META_REPO"
    exit 0
fi

echo ""
echo "🔍 检查配置..."
set -a; source "$ENV_FILE"; set +a

MISSING=()
for VAR in GITEA_BASE_URL GITEA_TOKEN_BOT AIFUSION_META_REPO; do
    if [ -z "${!VAR}" ]; then
        MISSING+=("$VAR")
    fi
done

if [ ${#MISSING[@]} -gt 0 ]; then
    echo "❌ 以下环境变量未配置，请编辑 $ENV_FILE："
    for V in "${MISSING[@]}"; do echo "   - $V"; done
    exit 1
fi

echo "✅ 所有必填配置项已就绪"
echo ""
echo "────────────────────────────────────"
echo "🎉 Skill-C 安装完成！"
echo ""
echo "说明："
echo "- 转录与AI纪要拉取由 tencent-meeting-skill 负责"
echo "- 两阶段 issue 抽取由 OpenClaw 负责"
echo "- 邮件发送由 imap-smtp-email 负责"
echo "- Skill-C 只负责 Gitea 状态更新 / 文件提交 / 日志"
