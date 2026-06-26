#!/bin/bash
# auto_topic_post_xiaohongshu.sh
# One-command flow: search-driven copywriting -> publish to Xiaohongshu
# Usage:
#   bash auto_topic_post_xiaohongshu.sh "主题"
#   bash auto_topic_post_xiaohongshu.sh "主题" "/tmp/openclaw/uploads/cover.jpg"

set -euo pipefail

TOPIC="${1:-}"
IMAGE_PATH="${2:-}"
ROOT_DIR="/Users/youke/.openclaw/workspace/skills/zeelin-xiaohongshu-autopost"
POST_SCRIPT="$ROOT_DIR/scripts/post_xiaohongshu.sh"

if [ -z "$TOPIC" ]; then
  echo "Error: topic is required"
  exit 1
fi

PROMPT="你是小红书爆文运营专家。围绕主题【${TOPIC}】先基于公开热点信号进行选题，再生成一篇软性带货小红书图文文案。必须包含人性驱动（痛点、损失厌恶、从众、即时收益）。\n\n要求：\n1) 先在脑内完成热点抽取与选题，选择最优角度；\n2) 标题14-20字，口语化，不夸张；\n3) 正文350-650字，结构：场景痛点->原因->3条解决路径->软性植入->结果->互动问题；\n4) 标签6-10个；\n5) 禁止硬广与绝对化承诺。\n\n输出格式必须严格如下，不要任何额外解释：\n<TITLE>标题</TITLE>\n<CONTENT>正文</CONTENT>\n<TAGS>标签1,标签2,标签3</TAGS>"

echo "Generating Xiaohongshu copy for topic: $TOPIC"
RESP_JSON="$(openclaw agent --agent main --message "$PROMPT" --json)"
TEXT="$(printf "%s" "$RESP_JSON" | jq -r '.result.payloads[0].text // empty')"

if [ -z "$TEXT" ]; then
  echo "Error: empty model output"
  exit 1
fi

TITLE="$(printf "%s" "$TEXT" | awk 'match($0, /<TITLE>.*<\/TITLE>/){s=substr($0,RSTART,RLENGTH); gsub(/<\/?TITLE>/, "", s); print s; exit}')"
CONTENT="$(printf "%s" "$TEXT" | awk '
  BEGIN{flag=0}
  /<CONTENT>/{
    flag=1
    sub(/.*<CONTENT>/, "")
  }
  flag{print}
  /<\/CONTENT>/{
    flag=0
  }
' | sed '$s:</CONTENT>.*::')"
TAGS_RAW="$(printf "%s" "$TEXT" | awk 'match($0, /<TAGS>.*<\/TAGS>/){s=substr($0,RSTART,RLENGTH); gsub(/<\/?TAGS>/, "", s); print s; exit}')"
TAGS_LINE="$(printf "%s" "$TAGS_RAW" | tr ',' '\n' | sed 's/^ *//;s/ *$//' | sed '/^$/d' | awk '{print "#" $0}' | paste -sd ' ' -)"

if [ -z "$TITLE" ] || [ -z "$CONTENT" ]; then
  echo "Error: model output missing <TITLE> or <CONTENT>"
  echo "Raw output:"
  echo "$TEXT"
  exit 1
fi

FINAL_CONTENT="$CONTENT"
if [ -n "$TAGS_LINE" ]; then
  printf -v FINAL_CONTENT "%s\n\n%s" "$CONTENT" "$TAGS_LINE"
fi

mkdir -p "$ROOT_DIR/output"
TS="$(date +%Y%m%d_%H%M%S)"
DRAFT_FILE="$ROOT_DIR/output/draft_${TS}.md"
{
  echo "# $TITLE"
  echo
  echo "$FINAL_CONTENT"
} > "$DRAFT_FILE"

echo "Draft saved: $DRAFT_FILE"

echo "Publishing..."
if [ -n "$IMAGE_PATH" ]; then
  bash "$POST_SCRIPT" "$TITLE" "$FINAL_CONTENT" "$IMAGE_PATH"
else
  bash "$POST_SCRIPT" "$TITLE" "$FINAL_CONTENT"
fi

echo "Done: topic -> copy -> publish flow completed"
