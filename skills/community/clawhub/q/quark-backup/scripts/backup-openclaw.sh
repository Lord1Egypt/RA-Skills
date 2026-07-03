#!/usr/bin/env bash
set -euo pipefail

OPENCLAW_HOME="${OPENCLAW_HOME:-/home/openclaw/.openclaw}"
WORKSPACE="${WORKSPACE:-$OPENCLAW_HOME/workspace}"
KUAKE_WRAPPER="${WORKSPACE}/tools/kuake/use-kuake.sh"
SECRET_FILE="${KUAKE_SECRET_FILE:-/home/openclaw/.config/openclaw-quark-backup.env}"
REMOTE_DIR="${KUAKE_REMOTE_DIR:-/openclaw}"
STAMP="$(TZ=Asia/Shanghai date '+%Y%m%d-%H%M%S')"
ARCHIVE="${TMPDIR:-/tmp}/openclaw-full-backup-${STAMP}.tar.gz"

cleanup() {
  rm -f "$ARCHIVE"
}
trap cleanup EXIT

if [[ ! -x "$KUAKE_WRAPPER" ]]; then
  echo "错误：找不到 kuake 包装脚本 $KUAKE_WRAPPER" >&2
  exit 1
fi

if [[ -f "$SECRET_FILE" ]]; then
  set -a
  source "$SECRET_FILE"
  set +a
fi

: "${KUAKE_COOKIE:?错误：未检测到 KUAKE_COOKIE，请先在 $SECRET_FILE 中配置 Cookie。}"

remote_parent="$(dirname "$REMOTE_DIR")"
remote_name="$(basename "$REMOTE_DIR")"
[[ "$remote_parent" == "." ]] && remote_parent="/"

printf '[1/4] 生成压缩包：%s\n' "$ARCHIVE"

tar \
  --warning=no-file-changed \
  --ignore-failed-read \
  --exclude='.openclaw/extensions/node_modules' \
  --exclude='.openclaw/extensions/*/node_modules' \
  --exclude='.openclaw/agents/*/workspace/node_modules' \
  --exclude='.openclaw/agents/*/workspace/.openclaw/chrome' \
  --exclude='.openclaw/agents/*/workspace/.openclaw/chrome/*' \
  --exclude='.openclaw/agents/*/workspace/.openclaw/chrome-deb' \
  --exclude='.openclaw/agents/*/workspace/.openclaw/chrome-deb/*' \
  --exclude='.openclaw/agents/*/workspace/.openclaw/browser-runtime' \
  --exclude='.openclaw/agents/*/workspace/.openclaw/browser-runtime/*' \
  --exclude='.openclaw/agents/*/workspace/.openclaw/cdp-profile' \
  --exclude='.openclaw/agents/*/workspace/.openclaw/cdp-profile/*' \
  --exclude='.openclaw/agents/*/workspace/.openclaw/cdp-profile-*' \
  --exclude='workspace/tools/kuake/.env' \
  -czf "$ARCHIVE" \
  -C "$(dirname "$OPENCLAW_HOME")" "$(basename "$OPENCLAW_HOME")"

ls -lh "$ARCHIVE"

printf '[2/4] 确保远端目录存在：%s\n' "$REMOTE_DIR"
"$KUAKE_WRAPPER" create "$remote_name" "$remote_parent" >/dev/null 2>&1 || true

remote_path="${REMOTE_DIR%/}/$(basename "$ARCHIVE")"
printf '[3/4] 上传到夸克：%s\n' "$remote_path"
"$KUAKE_WRAPPER" upload "$ARCHIVE" "$remote_path"

printf '[4/4] 校验远端文件\n'
if ! "$KUAKE_WRAPPER" list "$REMOTE_DIR" | grep -F "$(basename "$ARCHIVE")" >/dev/null; then
  echo "错误：远端校验失败，未找到 $(basename "$ARCHIVE")" >&2
  exit 1
fi

printf '备份完成：%s\n' "$remote_path"