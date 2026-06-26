#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROFILE_API="${WX_CHANNELS_PROFILE_API:-https://sph.litao.workers.dev/api/fetch_video_profile}"
QUALITY="${WX_CHANNELS_QUALITY:-h264}"

usage() {
  cat <<'USAGE'
Resolve and download a WeChat Channels share link without starting a local proxy.

Usage:
  download_sph.sh <https://weixin.qq.com/sph/...> [filename.mp4]

Environment:
  WX_CHANNELS_QUALITY      h264 or h265, default h264
  WX_CHANNELS_PROFILE_API  resolver API, default https://sph.litao.workers.dev/api/fetch_video_profile

Output:
  Downloads to ~/Downloads/<filename>.mp4 with curl. No local proxy, no binary install.
USAGE
}

if [[ $# -lt 1 || "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

share_url="$1"
filename="${2:-}"

case "$share_url" in
  https://weixin.qq.com/sph/*|http://weixin.qq.com/sph/*) ;;
  *)
    echo "Expected a weixin.qq.com/sph share URL, got: $share_url" >&2
    exit 2
    ;;
esac

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
profile="$tmp/profile.json"

curl -fsSL "$PROFILE_API" \
  -H 'content-type: application/json' \
  --data "$(python3 -c 'import json,sys; print(json.dumps({"url": sys.argv[1]}, ensure_ascii=False))' "$share_url")" \
  > "$profile"

QUALITY="$QUALITY" python3 - "$profile" "$share_url" "$tmp" <<'PY'
import json
import os
import re
import sys
from urllib.parse import urlparse

profile_path, share_url, out_dir = sys.argv[1], sys.argv[2], sys.argv[3]
with open(profile_path, "r", encoding="utf-8") as f:
    data = json.load(f)

if data.get("errCode") not in (None, 0):
    raise SystemExit(f"resolver errCode={data.get('errCode')}: {data.get('errMsg', '')}")

root = data.get("data") or {}
feed = root.get("feedInfo") or {}
author_info = root.get("authorInfo") or {}
quality = os.environ.get("QUALITY", "h264").lower()

if quality == "h265":
    video_url = (feed.get("h265VideoInfo") or {}).get("videoUrl") or feed.get("videoUrl")
else:
    video_url = (feed.get("h264VideoInfo") or {}).get("videoUrl") or feed.get("videoUrl")

if not video_url:
    raise SystemExit("resolver returned no video URL")

title = re.sub(r"\s+", " ", feed.get("description") or "").strip()
author = re.sub(r"\s+", " ", author_info.get("nickname") or "").strip()
slug = urlparse(share_url).path.rstrip("/").split("/")[-1] or "wx_channels_video"
safe_title = re.sub(r'[\\/:*?"<>|\r\n]+', "_", title)[:60].strip(" _")
suggested = f"{safe_title or slug}.mp4"

for name, value in {
    "video_url": video_url,
    "suggested_filename": suggested,
    "title": title or "-",
    "author": author or "-",
}.items():
    with open(os.path.join(out_dir, name), "w", encoding="utf-8") as f:
        f.write(value)
PY

video_url="$(cat "$tmp/video_url")"
suggested_filename="$(cat "$tmp/suggested_filename")"
title="$(cat "$tmp/title")"
author="$(cat "$tmp/author")"

if [[ -z "$filename" ]]; then
  filename="$suggested_filename"
fi

out="$HOME/Downloads/$filename"
mkdir -p "$HOME/Downloads"

echo "author: $author"
echo "title: $title"
echo "quality: $QUALITY"
echo "output: $out"

curl -fL --retry 2 --connect-timeout 20 -o "$out" "$video_url"
echo "downloaded: $out"
