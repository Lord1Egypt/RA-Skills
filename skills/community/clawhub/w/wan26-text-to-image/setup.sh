#!/bin/bash
# wan2.6 图片生成技能 - 将密钥写入本地 .env（已列入 .gitignore）
# 不在脚本中写入 ~/.zshrc / ~/.bashrc，避免密钥进入可被同步的 shell 配置

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/.env"

echo "=============================================="
echo "wan2.6 图片生成技能 - 配置向导"
echo "=============================================="
echo ""

echo "当前配置状态："
if [ -n "${DASHSCOPE_API_KEY:-}" ]; then
    echo "✅ 环境变量已配置（已脱敏）"
else
    echo "❌ 环境变量未配置"
fi

if [ -f "$ENV_FILE" ]; then
    echo "✅ 本地 .env 存在：$ENV_FILE"
else
    echo "❌ 本地 .env 不存在"
fi

echo ""
echo "=============================================="
echo "配置 API Key"
echo "=============================================="
echo ""

echo "请从阿里云百炼控制台创建密钥，并粘贴到下方。"
echo "获取说明：https://help.aliyun.com/zh/model-studio/get-api-key"
echo ""
read -r -p "API Key: " API_KEY

if [ -z "$API_KEY" ]; then
    echo "❌ API Key 不能为空"
    exit 1
fi

if [ "${#API_KEY}" -lt 8 ]; then
    echo "⚠️  密钥长度过短，请确认是否粘贴完整"
    read -r -p "是否继续保存？(y/n): " CONFIRM
    if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
        echo "已取消"
        exit 0
    fi
fi

cat > "$ENV_FILE" << EOF
# wan2.6 图片生成技能 - 本地密钥（勿提交仓库）
# 此文件由 setup.sh 生成，已加入 .gitignore
DASHSCOPE_API_KEY=$API_KEY
EOF

chmod 600 "$ENV_FILE"

echo ""
echo "✅ 已保存到：$ENV_FILE"
echo "   （不在终端打印密钥内容；长度 ${#API_KEY} 字符）"
echo ""
echo "下一步："
echo "  - 当前终端可执行：set -a && source \"$ENV_FILE\" && set +a"
echo "  - 或运行：python3 config.py"
echo "  - 勿将密钥复制到可提交的配置文件或截图中"
echo ""
