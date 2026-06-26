#!/bin/bash
# comment.sh — 在指定推文下回复一条评论
# Usage: bash comment.sh "评论内容" "https://x.com/user/status/123456" [base_url]

COMMENT="$1"
TWEET_URL="$2"
BASE_URL="${3:-https://x.com}"
CLI="openclaw browser"

if [ -z "$COMMENT" ] || [ -z "$TWEET_URL" ]; then
  echo "Usage: bash comment.sh \"评论内容\" \"推文URL\" [base_url]"
  exit 1
fi

echo "============================================"
echo "  Twitter/X 评论"
echo "============================================"
echo "URL: $TWEET_URL"
echo ""

echo "=== 打开推文页 ==="
$CLI open "$TWEET_URL" 2>/dev/null
sleep 3

echo "=== 查找回复框 ==="
SNAP=$($CLI snapshot 2>/dev/null)
REF=$(echo "$SNAP" | grep -iE 'textbox|placeholder.*[Rr]eply|placeholder.*回复|placeholder.*[Pp]ost' | grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//')

if [ -z "$REF" ]; then
  REF=$(echo "$SNAP" | grep -i 'contenteditable\|role="textbox"\|回复' | grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//')
fi

if [ -z "$REF" ]; then
  echo "ERROR: Could not find reply box"
  exit 1
fi

echo "  找到回复框 ref=$REF"
echo "=== 输入评论 ==="
$CLI type "$REF" "$COMMENT" 2>/dev/null
sleep 1

echo "=== 点击发送 ==="
SNAP2=$($CLI snapshot 2>/dev/null)
BTN=$(echo "$SNAP2" | grep -iE 'button.*[Rr]eply|button.*回复|button.*[Pp]ost' | grep -v 'disabled' | grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//')
if [ -z "$BTN" ]; then
  echo "  尝试 Cmd+Enter 发送"
  $CLI press "Meta+Enter" 2>/dev/null
else
  $CLI click "$BTN" 2>/dev/null
fi

sleep 2
echo "=== 完成 ==="
