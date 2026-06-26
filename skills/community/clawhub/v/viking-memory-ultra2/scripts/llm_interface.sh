#!/bin/bash
# Viking Memory System - LLM 接口模块
# I2: source guard - 防止直接执行
if [ -n "${BASH_SOURCE[0]}" ] && [ "${BASH_SOURCE[0]}" == "${0}" ]; then
    echo "错误: llm_interface.sh 应通过 source 加载, 而非直接执行"
    exit 1
fi

# LLM 接口模块 - 使用 MiniMax API 实现 LLM 功能
# 支持: 压缩, 回忆, 关键词提取, 轮廓生成

# ============ MiniMax API 配置 ============
MINIMAX_API_KEY="sk-cp-Sj_-2JKziYYMC6TrVs_Fur4vL7VYHH25ftjRU6Av7JWbudv02LE3vQKZF4HnhNBTesNdPSsXcJUQrJDjqPfHPI5UE7ROk6HY2Id7xj9b67isIld80uZPVsg"
MINIMAX_BASE_URL="https://api.minimaxi.com/anthropic/v1/messages"

# ============ 解析 LLM 响应 ============
parse_response() {
    python3 -c "
import json,sys
d = json.load(sys.stdin)
for c in d.get('content',[]):
    if c.get('type') == 'text':
        print(c.get('text',''), end='')
        break
else:
    print('解析失败')
"
}

# ============ JSON 安全转义 ============
json_escape() {
    python3 -c "
import sys, json
text = sys.stdin.read()[:8000]
# 使用 json.dumps 自动处理所有转义
print(json.dumps(text, ensure_ascii=False)[1:-1])
"
}

# ============ LLM 调用函数 ============

# 压缩记忆到目标层级
llm_compress() {
    local file="$1"
    local target_layer="$2"
    local content=$(cat "$file")
    
    # JSON 安全转义
    local safe_content=$(echo "$content" | json_escape)
    local prompt="你是一个记忆压缩助手。请将以下记忆内容压缩成${target_layer}层级的摘要，保留关键信息。回复格式：直接输出压缩后的内容，不要有前缀解释。记忆内容：${safe_content}"
    
    local response=$(curl -s --max-time 30 "$MINIMAX_BASE_URL" \
        -H "Content-Type: application/json" \
        -H "x-api-key: $MINIMAX_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -d "{
            \"model\": \"MiniMax-M2.5\",
            \"max_tokens\": 2000,
            \"messages\": [{\"role\":\"user\",\"content\":\"$prompt\"}]
        }" 2>/dev/null)
    
    echo "$response" | parse_response
}

# 从归档记忆恢复细节
llm_recall() {
    local archive_file="$1"
    local query="$2"
    
    # 读取内容
    local content=""
    if [ "$archive_file" = "/dev/stdin" ] || [ "$archive_file" = "stdin" ]; then
        content=$(cat)
    else
        content=$(cat "$archive_file" 2>/dev/null || echo "")
    fi
    
    # JSON 安全转义
    local safe_content=$(echo "$content" | json_escape)
    local prompt="你是一个记忆恢复助手。以下是归档的记忆内容，请根据查询 '${query}' 恢复相关细节，用自然语言回答。归档记忆：${safe_content}"
    
    local response=$(curl -s --max-time 30 "$MINIMAX_BASE_URL" \
        -H "Content-Type: application/json" \
        -H "x-api-key: $MINIMAX_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -d "{
            \"model\": \"MiniMax-M2.5\",
            \"max_tokens\": 1000,
            \"messages\": [{\"role\":\"user\",\"content\":\"$prompt\"}]
        }" 2>/dev/null)
    
    echo "$response" | parse_response
}

# 提取关键词
llm_extract_keywords() {
    local content="$1"
    
    # JSON 安全转义
    local safe_content=$(echo "$content" | json_escape)
    local prompt="从以下内容中提取5-10个关键词，直接输出关键词，用逗号分隔，不要解释：${safe_content}"
    
    local response=$(curl -s --max-time 30 "$MINIMAX_BASE_URL" \
        -H "Content-Type: application/json" \
        -H "x-api-key: $MINIMAX_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -d "{
            \"model\": \"MiniMax-M2.5\",
            \"max_tokens\": 500,
            \"messages\": [{\"role\":\"user\",\"content\":\"$prompt\"}]
        }" 2>/dev/null)
    
    echo "$response" | parse_response
}

# 生成轮廓摘要
llm_generate_contour() {
    local content="$1"
    
    # JSON 安全转义
    local safe_content=$(echo "$content" | json_escape)
    local prompt="用3-5句话概括以下内容的核心要点，直接输出摘要：${safe_content}"
    
    local response=$(curl -s --max-time 30 "$MINIMAX_BASE_URL" \
        -H "Content-Type: application/json" \
        -H "x-api-key: $MINIMAX_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -d "{
            \"model\": \"MiniMax-M2.5\",
            \"max_tokens\": 500,
            \"messages\": [{\"role\":\"user\",\"content\":\"$prompt\"}]
        }" 2>/dev/null)
    
    echo "$response" | parse_response
}

# 测试 LLM 连接
llm_test() {
    echo "=== Viking LLM 连接测试 ==="
    echo "Provider: MiniMax API"
    echo "Model: MiniMax-M2.5"
    
    # 测试一个简单的调用
    local response=$(curl -s --max-time 15 "$MINIMAX_BASE_URL" \
        -H "Content-Type: application/json" \
        -H "x-api-key: $MINIMAX_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -d '{
            "model": "MiniMax-M2.5",
            "max_tokens": 10,
            "messages": [{"role":"user","content":"Hi"}]
        }' 2>/dev/null)
    
    if echo "$response" | grep -q "MiniMax-M2.5"; then
        echo "✅ MiniMax API 连接成功"
    else
        echo "❌ MiniMax API 连接失败"
        echo "Response: $response"
    fi
}

# 导出函数
export -f llm_compress llm_recall llm_extract_keywords llm_generate_contour llm_test
