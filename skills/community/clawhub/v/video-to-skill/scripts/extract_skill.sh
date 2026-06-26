#!/bin/bash
# Step 4: Extract Skill content from video summary using LLM
# Usage: ./extract_skill.sh <summary_md_file> <output_md_file>
set -e

SUMMARY_FILE="$1"
OUTPUT_FILE="${2:-/tmp/generated_skill.md}"
MINIMAX_API_KEY="${MINIMAX_API_KEY:-}"

if [ -z "$SUMMARY_FILE" ]; then
  echo "ERROR: summary file is required"
  exit 1
fi

if [ ! -f "$SUMMARY_FILE" ]; then
  echo "ERROR: file not found: $SUMMARY_FILE"
  exit 1
fi

if [ -z "$MINIMAX_API_KEY" ]; then
  echo "ERROR: MINIMAX_API_KEY is not set"
  exit 1
fi

SUMMARY_CONTENT=$(cat "$SUMMARY_FILE")

echo "Extracting Skill from summary..."

RESPONSE=$(curl -s -X POST "https://api.minimax.chat/v1/chat/completions" \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(jq -n \
    --arg content "你是一个 Skill 设计助手。请根据以下视频摘要，生成一个标准的 OpenClaw SKILL.md 文件内容。

【视频摘要】
$SUMMARY_CONTENT

请生成以下格式的 Skill 内容：

\`\`\`markdown
---
name: [skill-name]  # 英文名，短横线分隔，最多64字符
description: [描述]  # 说明此 Skill 的功能和使用场景，when to use
---

# [技能标题]

[详细的工作流程、步骤说明、示例、注意事项等]
\`\`\`

要求：
1. name 只能包含小写字母、数字和连字符
2. description 要具体说明触发条件（何时使用此 Skill）
3. 正文要有可操作性，包含具体步骤
4. 不要输出多余解释，直接输出 Skill 内容
5. 尽量详细，工作流程要完整可执行" \
    '{
      model: "MiniMax-Text-01",
      messages: [{role: "user", content: $content}],
      temperature: 0.5,
      max_tokens: 4000
    }')")

SKILL_CONTENT=$(echo "$RESPONSE" | jq -r '.choices[0].message.content // empty')

if [ -z "$SKILL_CONTENT" ]; then
  echo "ERROR: LLM call failed"
  echo "$RESPONSE"
  exit 1
fi

# 提取 markdown 代码块中的内容（如果 LLM 返回了代码块）
if echo "$SKILL_CONTENT" | grep -q '```markdown'; then
  echo "$SKILL_CONTENT" | sed -n '/```markdown/,/```/p' | sed '1d;$d' > "$OUTPUT_FILE"
elif echo "$SKILL_CONTENT" | grep -q '```'; then
  echo "$SKILL_CONTENT" | sed -n '/```/,/```/p' | sed '1d;$d' > "$OUTPUT_FILE"
else
  echo "$SKILL_CONTENT" > "$OUTPUT_FILE"
fi

echo "SKILL_FILE=$OUTPUT_FILE"
