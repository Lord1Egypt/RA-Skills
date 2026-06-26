#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -lt 1 ]; then
  echo "usage: $0 <url>" >&2
  exit 2
fi
url="$1"
exec /usr/bin/google-chrome-stable   --headless=new   --disable-gpu   --no-sandbox   --virtual-time-budget=15000   --dump-dom   "$url"
