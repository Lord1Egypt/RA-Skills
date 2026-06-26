#!/bin/bash
# follow_back.sh — 在粉丝列表中点「关注」回关（只点显示为 Follow/关注 的按钮，不点 Following/已关注）
# Usage: bash follow_back.sh [username] [base_url] [max_count]
# Example: bash follow_back.sh Gsdata5566 https://x.com 10

USER="${1:-Gsdata5566}"
BASE_URL="${2:-https://x.com}"
MAX="${3:-10}"
CLI="openclaw browser"

echo "============================================"
echo "  Twitter/X 回关"
echo "============================================"
echo "账号: $USER | 最多回关: $MAX"
echo ""

echo "=== 打开粉丝列表 ==="
$CLI open "${BASE_URL}/${USER}/followers" 2>/dev/null
# 缩短等待以降低飞书等渠道 request timed out
sleep 5

ensure_followers_tab() {
  local url
  url=$($CLI evaluate --fn '() => location.href' 2>/dev/null || true)
  if echo "$url" | grep -q "verified_followers"; then
    $CLI navigate "${BASE_URL}/${USER}/followers" 2>/dev/null
    sleep 3
  fi
}

# 在「关注者」列表先滚动、再回关
echo "=== 处理「关注者」列表 ==="
# 确保停留在「关注者」列表（不要进入「认证关注者」）
ensure_followers_tab
$CLI press "PageDown" 2>/dev/null || true
sleep 1
$CLI press "PageDown" 2>/dev/null || true
sleep 1

# 仅在当前「关注者」列表回关（不切换到认证关注者）

do_follow_back() {
  local SNAP REF
  SNAP=$($CLI snapshot 2>/dev/null)
  REF=$(echo "$SNAP" | grep -E 'button.*"回关|button.*"Follow"|button.*"关注"' | grep -v 'Following\|已关注' | grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//')
  if [ -z "$REF" ]; then
    REF=$(echo "$SNAP" | grep -E 'Follow|关注|回关' | grep -v 'Following|已关注' | grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//')
  fi
  if [ -z "$REF" ]; then
    REF=$(echo "$SNAP" | grep -B1 -E ': Follow$|: 关注$|: 回关$|"Follow"|"关注"|"回关"' | grep -v 'Following|已关注' | grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//')
  fi
  if [ -z "$REF" ]; then
    REF=$(echo "$SNAP" | grep -B2 -E 'Follow|关注|回关' | grep -v 'Following|已关注' | grep -oE 'ref=e[0-9]+' | tail -1 | sed 's/ref=//')
  fi
  if [ -z "$REF" ]; then
    REF=$(echo "$SNAP" | grep -E 'cursor=pointer.*(Follow|回关)|(Follow|回关).*cursor=pointer' | grep -v Following | grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//')
  fi
  echo "$REF"
}

CLICKED=0
# 第一阶段：当前 tab（关注者列表）回关
for i in $(seq 1 "$MAX"); do
  ensure_followers_tab
  REF=$(do_follow_back)
  if [ -z "$REF" ]; then
    if [ $CLICKED -eq 0 ]; then
      SNAP=$($CLI snapshot 2>/dev/null)
      echo "  未找到 Follow/关注/回关 按钮。页面片段（供排查）："
      echo "$SNAP" | grep -iE "follow|关注|回关|button" | head -20
    fi
    break
  fi
  echo "  点击回关 ($((CLICKED+1))/$MAX) ref=$REF"
  $CLI click "$REF" 2>/dev/null
  CLICKED=$((CLICKED+1))
  sleep 1
done

# 第二阶段：不再切换「认证关注者」，避免遗漏关注者列表

if [ $CLICKED -eq 0 ]; then
  echo "  没有更多可回关的按钮，或页面结构变化。"
fi

echo ""
echo "=== 完成 ==="
echo "本次回关 $CLICKED 人。"
