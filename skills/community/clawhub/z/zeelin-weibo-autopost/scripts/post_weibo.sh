#!/usr/bin/env bash
# 微博网页版自动发布（排查版：更多日志与备用选择器）
# Usage: bash post_weibo.sh "微博内容"
# 使用前：浏览器登录 weibo.com，Browser Relay 挂上该标签页。

set -e
CONTENT="$1"
WEIBO_BASE="${WEIBO_BASE:-https://weibo.com}"
CLI="${OPENCLAW_CLI:-openclaw browser}"
SNAP_DEBUG="${SNAP_DEBUG:-/tmp/weibo_snap.txt}"

if [ -z "$CONTENT" ]; then
  echo "用法: $0 \"微博内容\""
  exit 1
fi
[ ${#CONTENT} -gt 2000 ] && CONTENT="${CONTENT:0:1997}..."

echo "============================================"
echo "  微博自动发布"
echo "============================================"
echo "内容长度: ${#CONTENT} 字"
echo ""

echo "=== Step 1: 打开微博 ==="
$CLI open "${WEIBO_BASE}" 2>/dev/null
sleep 6

echo "=== Step 2: 获取页面快照 ==="
SNAP=$($CLI snapshot 2>/dev/null)
echo "$SNAP" > "$SNAP_DEBUG"
echo "  快照已保存到 $SNAP_DEBUG（若失败可查看）"

# 点击「发微博」/「写微博」打开发布框（优先匹配发布入口，排除搜索）
SEND_REF=$(echo "$SNAP" | grep -E '发微博|写微博' | grep -v '搜索' | grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//')
if [ -z "$SEND_REF" ]; then
  SEND_REF=$(echo "$SNAP" | grep -E 'button.*发微博|button.*写微博' | grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//')
fi
if [ -z "$SEND_REF" ]; then
  SEND_REF=$(echo "$SNAP" | grep -E '发微博|写微博' | grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//')
fi

if [ -n "$SEND_REF" ]; then
  echo "=== Step 3: 点击发微博入口 ref=$SEND_REF ==="
  $CLI click "$SEND_REF" 2>/dev/null
  sleep 4
  SNAP=$($CLI snapshot 2>/dev/null)
  echo "$SNAP" >> "$SNAP_DEBUG"
else
  echo "  未找到「发微博」按钮，尝试直接找输入框（可能已在首页发布框）"
fi

echo "=== Step 4: 查找输入框 ==="
# 优先：说点什么、分享新鲜事（排除搜索框）
INPUT_REF=$(echo "$SNAP" | grep -E '说点什么|分享新鲜事|分享你的' | grep -v '搜索' | grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//')
if [ -z "$INPUT_REF" ]; then
  INPUT_REF=$(echo "$SNAP" | grep -E 'contenteditable|textbox|textarea' | grep -v '搜索' | grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//')
fi
if [ -z "$INPUT_REF" ]; then
  INPUT_REF=$(echo "$SNAP" | grep -i 'placeholder.*输入\|placeholder.*说' | grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//')
fi
if [ -z "$INPUT_REF" ]; then
  # 取任意可编辑区域（可能误点到搜索，但先尝试）
  INPUT_REF=$(echo "$SNAP" | grep -E 'textbox|contenteditable|textarea' | grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//')
fi

if [ -z "$INPUT_REF" ]; then
  echo "ERROR: 未找到发微博输入框。"
  echo "请检查：1) 已登录 weibo.com  2) Browser Relay 已挂上该标签页  3) 页面已完全加载"
  echo "快照片段（含 发微博/输入/textbox）："
  echo "$SNAP" | grep -iE '发微博|写微博|textbox|contenteditable|输入|说点' | head -20
  exit 1
fi

echo "  使用输入框 ref=$INPUT_REF"
echo "=== Step 5: 填入正文 ==="
$CLI type "$INPUT_REF" "$CONTENT" 2>/dev/null
sleep 2

echo "=== Step 6: 查找并点击发布按钮 ==="
SNAP=$($CLI snapshot 2>/dev/null)
POST_REF=$(echo "$SNAP" | grep -E '"发布"|"发微博"|发布' | grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//')
if [ -z "$POST_REF" ]; then
  POST_REF=$(echo "$SNAP" | grep -E 'button.*发布|发布.*button' | grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//')
fi
if [ -z "$POST_REF" ]; then
  POST_REF=$(echo "$SNAP" | grep -E '发送|发微博' | grep -v '写微博' | grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//')
fi

if [ -n "$POST_REF" ]; then
  echo "  点击发布 ref=$POST_REF"
  $CLI click "$POST_REF" 2>/dev/null
  sleep 2
  echo "  已点击发布按钮。"
else
  echo "  未找到发布按钮，尝试快捷键 Ctrl+Enter / Cmd+Enter"
  $CLI press "Control+Enter" 2>/dev/null || $CLI press "Meta+Enter" 2>/dev/null
  sleep 2
fi

echo ""
echo "=== 完成 ==="
echo "请到微博页面确认是否出现「发布成功」或新微博。若未成功，可查看 $SNAP_DEBUG 排查页面结构。"
