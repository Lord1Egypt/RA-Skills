#!/bin/bash
# 四平台冒烟联测（固定短文案，不跑 generate_content）
set -uo pipefail

export OPENCLAW_CDP_PORT="${OPENCLAW_CDP_PORT:-9222}"
SKILLS="${OPENCLAW_SKILLS_ROOT:-$HOME/.openclaw/workspace/skills}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=/dev/null
source "${SCRIPT_DIR}/_thuqx_cdp_common.sh"

STAMP="$(date +%Y%m%d-%H%M)"
TEST_TAG="[四平台联测 $STAMP 可删]"

thuqx_ensure_cdp || exit 1

FAIL=0
PAUSE="${THUQX_PLATFORM_PAUSE:-2}"

echo "=== 1/4 X (Twitter) ==="
bash "$SKILLS/zeelin-twitter-web-autopost/scripts/tweet.sh" \
  "$TEST_TAG 自动化联测：X 正常 #OpenClaw #Test" "https://x.com" || FAIL=$((FAIL + 1))
sleep "$PAUSE"

echo "=== 2/4 Weibo ==="
python3 "$SKILLS/zeelin-weibo-autopost/scripts/cdp_weibo_ops.py" \
  "$TEST_TAG 自动化联测：微博/CDP OpenClaw" || FAIL=$((FAIL + 1))
sleep "$PAUSE"

echo "=== 3/4 Xiaohongshu ==="
python3 "$SKILLS/zeelin-xiaohongshu-autopost/scripts/cdp_xhs_publish_v5.py" \
  "$TEST_TAG 小红书联测" \
  "正文：四平台自动化联测（长文流：写长文→排版→发布）。" || FAIL=$((FAIL + 1))
sleep "$PAUSE"

echo "=== 4/4 WeChat MP (draft) ==="
python3 "$SKILLS/zeelin-wechat-autopost/scripts/cdp_wechat_publish_v10.py" \
  "$TEST_TAG 公众号联测" \
  "正文：四平台自动化联测。请在后台核对草稿。" || FAIL=$((FAIL + 1))

echo "=== Done. FAIL=$FAIL — 请各平台核对实际可见性 ==="
[ "$FAIL" -gt 0 ] && exit 1
exit 0
