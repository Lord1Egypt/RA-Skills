#!/bin/bash
# Viking Memory System - sv_archive_summary
# Phase 3: Archive 多粒度摘要生成
#
# 用法:
#   sv_archive_summary.sh <file> [--keep]

set +e

VIKING_HOME="${VIKING_HOME:-$HOME/.openclaw/viking}"

FILE="$1"
KEEP_FULL=false

[ -z "$FILE" ] && { echo "用法: sv_archive_summary.sh <file> [--keep]"; exit 1; }
[ ! -f "$FILE" ] && { echo "文件不存在: $FILE"; exit 1; }

if [ "$2" = "--keep" ]; then
    KEEP_FULL=true
fi

echo "=== Phase 3: Archive 摘要生成 ==="
echo "文件: $(basename "$FILE")"

# ============ 读取内容 ============
CONTENT=$(sed -n '/^---$/,/^---$/d; p' "$FILE" 2>/dev/null)
[ -z "$CONTENT" ] && { echo "⚠ 文件无正文内容"; exit 1; }

# ============ 生成多粒度摘要 ============
echo "正在调用 LLM 生成摘要..."

# API 配置
API_URL="https://integrate.api.nvidia.com/v1/chat/completions"
API_KEY="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"
MODEL="qwen/qwen3.5-122b-a10b"

# 构建 prompt
PROMPT="你是一个记忆压缩专家。请为以下记忆内容生成多粒度摘要。
回复格式：
===ONE_SENTENCE===
[一句话摘要，最多20字]
===PARAGRAPH===
[段落摘要，最多100字]

原文：
$CONTENT"

# JSON 转义
SAFE_PROMPT=$(python3 -c "import json,sys; print(json.dumps(sys.stdin.read()))" <<< "$PROMPT" | sed 's/^"//; s/"$//')

# 调用 LLM
RESPONSE=$(curl -s --max-time 30 "$API_URL" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"model\":\"$MODEL\",\"max_tokens\":500,\"temperature\":0.3,\"messages\":[{\"role\":\"user\",\"content\":$SAFE_PROMPT}]}" 2>/dev/null)

# 解析响应
LLM_CONTENT=$(echo "$RESPONSE" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('choices', [{}])[0].get('message', {}).get('content', ''))
except: print('')
" 2>/dev/null)

# 提取摘要
ONE_SENTENCE=$(echo "$LLM_CONTENT" | grep -A1 "===ONE_SENTENCE===" | tail -1 | sed 's/^[[:space:]]*//; s/[[:space:]]*$//' | head -c 100)
PARAGRAPH=$(echo "$LLM_CONTENT" | grep -A1 "===PARAGRAPH===" | tail -1 | sed 's/^[[:space:]]*//; s/[[:space:]]*$//' | head -c 300)

[ -z "$ONE_SENTENCE" ] && ONE_SENTENCE="记忆摘要"
[ -z "$PARAGRAPH" ] && PARAGRAPH="${CONTENT:0:200}..."

echo ""
echo "【一句话摘要】$ONE_SENTENCE"
echo "【段落摘要】$PARAGRAPH"

# ============ 保存 ============
FULL_FILE="${FILE}.archive.full"
SUMMARY_ESCAPED=$(python3 -c "import json; print(json.dumps('$ONE_SENTENCE | $PARAGRAPH')[1:-1])" 2>/dev/null || echo "$ONE_SENTENCE | $PARAGRAPH")

# 使用 awk 更新 frontmatter
awk -v summary="$SUMMARY_ESCAPED" -v keep_full="$KEEP_FULL" '
/^---$/ { in_fm=1; print; next }
/^---$/ && in_fm { 
    in_fm=0
    print "summary: \"" summary "\""
    if (keep_full == "true")
        print "full_content_file: " substr(FILENAME, length(FILENAME)-length(basename(FILENAME)))
    print; next 
}
in_fm && /^summary:/ { next }
in_fm && /^full_content_file:/ { next }
in_fm && /^last_access:/ { print; next }
/^[^#]/ { 
    if (in_fm && keep_full == "true") {
        print "summary: \"" summary "\""
        print "full_content_file: " FILENAME ".archive.full"
    }
    in_fm=0
}
{ print }
' "$FILE" > "${FILE}.tmp" && mv "${FILE}.tmp" "$FILE"

# 保存完整内容
if [ "$KEEP_FULL" = true ]; then
    echo "$CONTENT" > "$FULL_FILE"
    echo "✓ 完整内容已保存到: $(basename "$FULL_FILE")"
fi

echo "✓ 摘要已添加到 frontmatter"
echo "=== 完成 ==="
exit 0
