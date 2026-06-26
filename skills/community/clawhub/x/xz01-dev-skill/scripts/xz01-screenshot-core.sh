#!/usr/bin/env bash
set -euo pipefail
OUT_DIR="${1:-/root/.hermes/workspace/xz01-factory/test-artifacts/screenshots}"
mkdir -p "$OUT_DIR"
CHROME_BIN="${CHROME_BIN:-$(command -v chromium-browser || command -v chromium || command -v google-chrome || true)}"
if [[ -z "$CHROME_BIN" ]]; then echo "FAIL chromium_not_found" >&2; exit 2; fi
capture(){
  local name="$1" url="$2" width="$3" height="$4" ua="$5"
  "$CHROME_BIN" --headless --no-sandbox --disable-gpu --hide-scrollbars --ignore-certificate-errors \
    --window-size="${width},${height}" --user-agent="$ua" --screenshot="$OUT_DIR/${name}.png" "$url" >/dev/null 2>&1 || {
      echo "FAIL screenshot $name $url" >&2; return 1; }
  echo "$OUT_DIR/${name}.png"
}
PC_UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125 Safari/537.36'
M_UA='Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 Version/17.4 Mobile/15E148 Safari/604.1'
capture pc-home https://www.900az.com/ 1440 1400 "$PC_UA"
capture pc-soft-list https://www.900az.com/azos/ 1440 1400 "$PC_UA"
capture pc-game-list https://www.900az.com/gzos/ 1440 1400 "$PC_UA"
capture pc-news-list https://www.900az.com/zoszx04/ 1440 1400 "$PC_UA"
capture m-home https://m.900az.com/ 390 1400 "$M_UA"
capture m-soft-list https://m.900az.com/azos/ 390 1400 "$M_UA"
capture m-game-list https://m.900az.com/gzos/ 390 1400 "$M_UA"
capture m-news-list https://m.900az.com/zoszx04/ 390 1400 "$M_UA"
