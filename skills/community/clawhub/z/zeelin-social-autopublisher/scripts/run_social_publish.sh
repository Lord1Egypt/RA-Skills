#!/bin/bash
# 旧版：固定「标题 + 同一段正文」发往四平台。
# 推荐：run_social_publish_v5.sh "主题"
set -euo pipefail

TITLE="${1:-}"
BODY="${2:-}"
if [ -z "$TITLE" ] || [ -z "$BODY" ]; then
  echo "Usage: run_social_publish.sh \"title\" \"body\""
  echo "Better: $(dirname "$0")/run_social_publish_v5.sh \"主题\""
  exit 1
fi

BASE="${OPENCLAW_SKILLS_ROOT:-$HOME/.openclaw/workspace/skills}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=/dev/null
source "${SCRIPT_DIR}/_thuqx_cdp_common.sh"
PAUSE="${THUQX_PLATFORM_PAUSE:-2}"

thuqx_ensure_cdp || exit 1

echo "[deprecated] Sequential title/body publish..."

echo "[1/4] Twitter..."
bash "$BASE/zeelin-twitter-web-autopost/scripts/tweet.sh" "$BODY"
sleep "$PAUSE"

echo "[2/4] Weibo Ops..."
bash "$BASE/zeelin-weibo-autopost/scripts/run_weibo_ops.sh" "$BODY"
sleep "$PAUSE"

echo "[3/4] Xiaohongshu..."
python3 "$BASE/zeelin-xiaohongshu-autopost/scripts/cdp_xhs_publish_v5.py" "$TITLE" "$BODY"
sleep "$PAUSE"

echo "[4/4] WeChat (draft)..."
python3 "$BASE/zeelin-wechat-autopost/scripts/cdp_wechat_publish_v10.py" "$TITLE" "$BODY"

echo "Done."
