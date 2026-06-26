#!/usr/bin/env bash
# Fetch a WeChat article HTML with browser-like headers
# Usage: fetch.sh <url> [output_file]
# If output_file is omitted, outputs to stdout

set -euo pipefail

URL="$1"
OUTPUT="${2:--}"

curl -sL \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36" \
  -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
  -H "Accept-Language: zh-CN,zh;q=0.9,en;q=0.8" \
  -o "$OUTPUT" \
  "$URL"
