#!/bin/zsh
# vwu.ai 模型调用脚本

set -e

VWU_API_KEY="${VWU_API_KEY:-}"
VWU_BASE_URL="${VWU_BASE_URL:-https://vwu.ai}"

if [ -z "$VWU_API_KEY" ]; then
    echo "❌ 错误: 未设置 VWU_API_KEY"
    echo ""
    echo "请按以下步骤获取 API key:"
    echo "1. 访问 https://vwu.ai"
    echo "2. 登录并进入控制台"
    echo "3. 在「令牌」页面生成新的 API key"
    echo "4. 设置环境变量: export VWU_API_KEY='your-key'"
    exit 1
fi

MODEL="${1:-}"
PROMPT="${2:-}"

if [ -z "$MODEL" ] || [ -z "$PROMPT" ]; then
    echo "用法: vwu-chat <model> <prompt>"
    echo ""
    echo "可用模型:"
    cat "$(dirname "$0")/models.txt" | sed 's/^/  - /'
    exit 1
fi

# 调用 API
response=$(curl -s "$VWU_BASE_URL/v1/chat/completions" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $VWU_API_KEY" \
    -d "{
        \"model\": \"$MODEL\",
        \"messages\": [{\"role\": \"user\", \"content\": \"$PROMPT\"}],
        \"stream\": false
    }")

# 检查错误
if echo "$response" | jq -e '.error' > /dev/null 2>&1; then
    error_msg=$(echo "$response" | jq -r '.error.message')
    echo "❌ API 错误: $error_msg"

    # 检查是否是额度问题
    if echo "$error_msg" | grep -iE "额度|quota|余额|用尽" > /dev/null; then
        echo ""
        echo "⚠️  API key 额度不足！"
        echo ""
        echo "解决方法:"
        echo "1. 访问 https://vwu.ai 控制台"
        echo "2. 为当前 key 充值，或"
        echo "3. 生成新的 API key 并更新环境变量"
        echo ""
        echo "当前 key: ${VWU_API_KEY:0:8}***"
    fi
    exit 1
fi

# 输出结果
echo "$response" | jq -r '.choices[0].message.content'
