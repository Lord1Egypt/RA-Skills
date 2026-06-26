#!/bin/bash
set -e

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_DIR="$HOME/.config/skill-b-pre-brief"
ENV_FILE="$CONFIG_DIR/.env"

echo "🚀 设置 Skill-B (pre_brief)..."
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
    echo "  - GITEA_ROUTINE_REPORT_PATH（gitea-routine-report 的安装目录）"
    exit 0
fi

echo ""
echo "🔍 检查配置..."
set -a; source "$ENV_FILE"; set +a

MISSING=()
for VAR in GITEA_BASE_URL GITEA_TOKEN_BOT AIFUSION_META_REPO GITEA_ROUTINE_REPORT_PATH; do
    if [ -z "${!VAR}" ]; then
        MISSING+=("$VAR")
    fi
done

if [ ${#MISSING[@]} -gt 0 ]; then
    echo "❌ 以下环境变量未配置，请编辑 $ENV_FILE："
    for V in "${MISSING[@]}"; do echo "   - $V"; done
    exit 1
fi

if [ ! -f "$GITEA_ROUTINE_REPORT_PATH/scripts/generate_report.py" ]; then
    echo "❌ GITEA_ROUTINE_REPORT_PATH 路径下未找到 scripts/generate_report.py"
    echo "   请确认 gitea-routine-report skill 已安装，并填写正确路径"
    exit 1
fi

echo "✅ 所有必填配置项已就绪"
echo ""
echo "────────────────────────────────────"
echo "🎉 Skill-B 安装完成！"
echo ""
echo "说明："
echo "- cron 建议：*/15 * * * * node $(pwd)/main.js scan | openclaw-trigger skill-b-pre-brief"
echo "- 或在 OpenClaw 的定时任务配置中添加此 skill 的 cron 触发"
echo "- AI 分析由 OpenClaw 负责"
echo "- 报告渲染由 gitea-routine-report 负责"
echo "- 邮件发送由 imap-smtp-email 负责"
echo "- Skill-B 只负责 Gitea 扫描 / 状态更新 / 日志"
