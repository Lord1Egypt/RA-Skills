#!/bin/bash
set -u -o pipefail

TITLE="${1:-}"
CONTENT="${2:-}"
IMAGE_PATH="${3:-/Users/youke/.openclaw/workspace/skills/zeelin-xiaohongshu-autopost/assets/default_cover.jpg}"
CLI="${OPENCLAW_CLI:-agent-browser}"
BASE_URL="https://creator.xiaohongshu.com/new/home"

if [ -z "$TITLE" ] || [ -z "$CONTENT" ]; then
  echo "Error: title and content are required."
  exit 1
fi

TITLE_SAFE="$(printf '%s' "$TITLE" | tr '\n' ' ' | sed 's/[[:space:]]\+/ /g')"
TITLE_SAFE="${TITLE_SAFE:0:64}"

get_snapshot() {
  local s
  s="$($CLI snapshot 2>/dev/null || true)"
  [ -z "$s" ] && s="$($CLI snapshot --interactive 2>/dev/null || true)"
  printf "%s" "$s"
}

extract_ref() {
  grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//' || true
}

find_publish_entry_ref() {
  echo "$1" | rg -n '发布笔记' -C 2 | rg '\[cursor=pointer\]' | head -1 | extract_ref
}

find_long_form_ref() {
  echo "$1" | rg -m1 '写长文' | extract_ref
}

find_cancel_ref() {
  local r
  r="$(echo "$1" | rg -m1 'button.*取消' | extract_ref)"
  [ -z "$r" ] && r="$(echo "$1" | rg -m1 '\[cursor=pointer\].*取消' | extract_ref)"
  printf "%s" "$r"
}

find_new_creation_ref() {
  local r
  r="$(echo "$1" | rg -m1 'button "新的创作"' | extract_ref)"
  [ -z "$r" ] && r="$(echo "$1" | rg -n '新的创作' -C 2 | rg '\[cursor=pointer\]' | head -1 | extract_ref)"
  printf "%s" "$r"
}

find_title_ref() {
  local r
  r="$(echo "$1" | rg -m1 'textbox.*(输入标题|填写标题)' | extract_ref)"
  [ -z "$r" ] && r="$(echo "$1" | rg -m1 '(输入标题|填写标题)' | extract_ref)"
  printf "%s" "$r"
}

find_content_ref() {
  local r
  r="$(echo "$1" | rg -m1 'paragraph.*(粘贴到这里|输入正文|输入文字)' | extract_ref)"
  [ -z "$r" ] && r="$(echo "$1" | rg -m1 'textbox.*输入正文' | extract_ref)"
  [ -z "$r" ] && r="$(echo "$1" | rg -m1 'paragraph.*正文描述' | extract_ref)"
  printf "%s" "$r"
}

find_layout_ref() {
  echo "$1" | rg -m1 '(button|generic).*(一键排版)' | extract_ref
}

find_basic_template_ref() {
  local r
  r="$(echo "$1" | rg -m1 '基础简约' | extract_ref)"
  [ -z "$r" ] && r="$(echo "$1" | rg -m1 '清晰明朗|黑白极简|轻感明快|文艺清新|平实叙事|素雅底纹' | extract_ref)"
  [ -z "$r" ] && r="$(echo "$1" | rg -m1 '模板封面' | extract_ref)"
  printf "%s" "$r"
}

find_next_ref() {
  echo "$1" | rg -m1 'button "下一步"' | extract_ref
}

find_publish_ref() {
  local r
  r="$(echo "$1" | rg -m1 'button "发布"' | extract_ref)"
  [ -z "$r" ] && r="$(echo "$1" | rg -m1 '(button|generic).*发布' | rg -v '发布笔记|发布图文笔记|发布视频笔记' | extract_ref)"
  printf "%s" "$r"
}

is_login_required() {
  echo "$1" | rg -q '手机号|验证码|登录|扫码登录|请先登录'
}

echo "Starting browser..."
$CLI start >/dev/null 2>&1 || true
$CLI status >/dev/null 2>&1 || { echo "Error: OpenClaw browser relay unavailable."; exit 1; }

echo "Opening Xiaohongshu creator page..."
$CLI open "$BASE_URL" >/dev/null 2>&1 || true
sleep 2 >/dev/null 2>&1 || sleep 2

SNAPSHOT="$(get_snapshot)"
is_login_required "$SNAPSHOT" && { echo "Error: Login required."; exit 1; }

PUBLISH_ENTRY_REF="$(find_publish_entry_ref "$SNAPSHOT")"
[ -z "$PUBLISH_ENTRY_REF" ] && { echo "Error: Publish entry not found."; exit 1; }

echo "Clicking 发布笔记: $PUBLISH_ENTRY_REF"
$CLI click "$PUBLISH_ENTRY_REF" >/dev/null 2>&1 || true
sleep 1 >/dev/null 2>&1 || sleep 1

SNAPSHOT="$(get_snapshot)"
LONG_REF="$(find_long_form_ref "$SNAPSHOT")"
[ -z "$LONG_REF" ] && { echo "Error: 写长文 entry not found."; exit 1; }

echo "Clicking 写长文: $LONG_REF"
$CLI click "$LONG_REF" >/dev/null 2>&1 || true
sleep 2 >/dev/null 2>&1 || sleep 2

SNAPSHOT="$(get_snapshot)"
CANCEL_REF="$(find_cancel_ref "$SNAPSHOT")"
if [ -n "$CANCEL_REF" ]; then
  echo "Closing popup via 取消: $CANCEL_REF"
  $CLI click "$CANCEL_REF" >/dev/null 2>&1 || true
  sleep 1 >/dev/null 2>&1 || sleep 1
  SNAPSHOT="$(get_snapshot)"
fi

NEW_REF="$(find_new_creation_ref "$SNAPSHOT")"
[ -z "$NEW_REF" ] && { echo "Error: 新的创作 button not found."; exit 1; }

echo "Clicking 新的创作: $NEW_REF"
$CLI click "$NEW_REF" >/dev/null 2>&1 || true
sleep 3 >/dev/null 2>&1 || sleep 3

TITLE_REF=""
CONTENT_REF=""
for _ in 1 2 3 4 5; do
  SNAPSHOT="$(get_snapshot)"
  TITLE_REF="$(find_title_ref "$SNAPSHOT")"
  CONTENT_REF="$(find_content_ref "$SNAPSHOT")"
  if [ -n "$TITLE_REF" ] && [ -n "$CONTENT_REF" ]; then
    break
  fi
  sleep 1 >/dev/null 2>&1 || sleep 1
done

[ -z "$TITLE_REF" ] && { echo "Error: title input not found."; exit 1; }
[ -z "$CONTENT_REF" ] && { echo "Error: content editor not found."; exit 1; }

echo "Typing title into $TITLE_REF"
$CLI click "$TITLE_REF" >/dev/null 2>&1 || true
$CLI press "Meta+A" >/dev/null 2>&1 || true
$CLI press "Control+A" >/dev/null 2>&1 || true
$CLI type "$TITLE_REF" "$TITLE_SAFE" >/dev/null 2>&1 || true
sleep 1 >/dev/null 2>&1 || sleep 1

echo "Typing content into $CONTENT_REF"
$CLI click "$CONTENT_REF" >/dev/null 2>&1 || true
$CLI press "Meta+A" >/dev/null 2>&1 || true
$CLI press "Control+A" >/dev/null 2>&1 || true
$CLI type "$CONTENT_REF" "$CONTENT" >/dev/null 2>&1 || true
sleep 1 >/dev/null 2>&1 || sleep 1

SNAPSHOT="$(get_snapshot)"
LAYOUT_REF="$(find_layout_ref "$SNAPSHOT")"
if [ -n "$LAYOUT_REF" ]; then
  echo "Clicking 一键排版: $LAYOUT_REF"
  $CLI click "$LAYOUT_REF" >/dev/null 2>&1 || true
  sleep 4 >/dev/null 2>&1 || sleep 4
fi

SNAPSHOT="$(get_snapshot)"
TEMPLATE_REF="$(find_basic_template_ref "$SNAPSHOT")"
if [ -n "$TEMPLATE_REF" ]; then
  echo "Selecting template: $TEMPLATE_REF"
  $CLI click "$TEMPLATE_REF" >/dev/null 2>&1 || true
  sleep 1 >/dev/null 2>&1 || sleep 1
fi

NEXT_REF=""
for _ in 1 2 3 4 5; do
  SNAPSHOT="$(get_snapshot)"
  NEXT_REF="$(find_next_ref "$SNAPSHOT")"
  [ -n "$NEXT_REF" ] && break
  $CLI press "PageDown" >/dev/null 2>&1 || true
  sleep 1 >/dev/null 2>&1 || sleep 1
done

[ -z "$NEXT_REF" ] && { echo "Error: 下一步 button not found."; exit 1; }

echo "Clicking 下一步: $NEXT_REF"
$CLI click "$NEXT_REF" >/dev/null 2>&1 || true
sleep 3 >/dev/null 2>&1 || sleep 3

PUBLISH_REF=""
for _ in 1 2 3 4 5; do
  SNAPSHOT="$(get_snapshot)"
  PUBLISH_REF="$(find_publish_ref "$SNAPSHOT")"
  [ -n "$PUBLISH_REF" ] && break
  $CLI press "PageDown" >/dev/null 2>&1 || true
  sleep 1 >/dev/null 2>&1 || sleep 1
done

[ -z "$PUBLISH_REF" ] && { echo "Error: 发布 button not found."; exit 1; }

echo "Clicking 发布: $PUBLISH_REF"
$CLI click "$PUBLISH_REF" >/dev/null 2>&1 || true
sleep 2 >/dev/null 2>&1 || sleep 2

# Handle confirmation dialog (确认发布 / 确认 / 继续发布)
find_confirm_ref() {
  local r
  r="$(echo "$1" | rg -m1 'button "确认发布"' | extract_ref)"
  [ -z "$r" ] && r="$(echo "$1" | rg -m1 'button "确认"' | extract_ref)"
  [ -z "$r" ] && r="$(echo "$1" | rg -m1 'button "继续发布"' | extract_ref)"
  [ -z "$r" ] && r="$(echo "$1" | rg -m1 'button "确定"' | extract_ref)"
  [ -z "$r" ] && r="$(echo "$1" | rg -m1 '(button|generic).*(确认发布|确认|继续发布|确定发布)' | extract_ref)"
  printf "%s" "$r"
}

SNAPSHOT="$(get_snapshot)"
CONFIRM_REF="$(find_confirm_ref "$SNAPSHOT")"
if [ -n "$CONFIRM_REF" ]; then
  echo "Clicking 确认发布: $CONFIRM_REF"
  $CLI click "$CONFIRM_REF" >/dev/null 2>&1 || true
  sleep 3 >/dev/null 2>&1 || sleep 3
fi

SUCCESS=0
for _ in 1 2 3 4 5 6 7 8; do
  SNAPSHOT="$(get_snapshot)"
  if echo "$SNAPSHOT" | rg -q '发布成功|审核中|已发布|内容已提交|笔记已发布'; then
    SUCCESS=1
    break
  fi
  # Retry confirm dialog if still on page
  CONFIRM_REF="$(find_confirm_ref "$SNAPSHOT")"
  if [ -n "$CONFIRM_REF" ]; then
    echo "Retrying 确认: $CONFIRM_REF"
    $CLI click "$CONFIRM_REF" >/dev/null 2>&1 || true
  fi
  sleep 2 >/dev/null 2>&1 || sleep 2
done

if [ "$SUCCESS" -eq 1 ]; then
  echo "Xiaohongshu publish flow completed successfully."
else
  echo "Publish clicked; success text not detected yet. Please verify in creator center."
fi
