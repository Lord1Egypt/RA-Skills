#!/bin/bash
# 文生图脚本 - 使用阿里云DashScope Wan2.6-t2i模型

# 参数检查
if [ -z "$1" ]; then
    echo "Usage: $0 <prompt> [negative_prompt] [size]"
    echo "Example: $0 '一间有着精致窗户的花店' '' '1280*1280'"
    exit 1
fi

PROMPT="$1"
NEGATIVE_PROMPT="${2:-}"
SIZE="${3:-1280*1280}"

# 检查API Key
if [ -z "$DASHSCOPE_API_KEY" ]; then
    echo "Error: DASHSCOPE_API_KEY environment variable is not set"
    exit 1
fi

# 调用API
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--data "{
    \"model\": \"wan2.6-t2i\",
    \"input\": {
        \"messages\": [
            {
                \"role\": \"user\",
                \"content\": [
                    {
                        \"text\": \"$PROMPT\"
                    }
                ]
            }
        ]
    },
    \"parameters\": {
        \"prompt_extend\": true,
        \"watermark\": false,
        \"n\": 1,
        \"negative_prompt\": \"$NEGATIVE_PROMPT\",
        \"size\": \"$SIZE\"
    }
}"