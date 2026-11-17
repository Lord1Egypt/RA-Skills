#!/usr/bin/env bash
# mermaid-export.sh — reading-notes-master v2.3 图形资产管线 B4
# mermaid 图表源(.mmd/.md) → SVG/PNG/PDF，绕开 mmdc 12 的 -w/-H 坑（用 -s 缩放），
# 且不下载 Chromium（PUPPETEER_SKIP_DOWNLOAD + 指向本机 Chrome）。
# 用法: mermaid-export.sh <input.mmd> [output-basename] [--scale 2] [--fmt svg,png,pdf]
set -euo pipefail

[ $# -lt 1 ] && { echo "Usage: $0 <input.mmd> [basename] [--scale N] [--fmt svg,png,pdf]"; exit 1; }
IN="$1"; BASE="${2:-${IN%.*}}"; SCALE=2; FMTS="svg"
shift || true
while [ $# -gt 0 ]; do
  case "$1" in
    --scale) SCALE="$2"; shift 2;;
    --fmt) FMTS="$2"; shift 2;;
    *) shift;;
  esac
done
[ -f "$IN" ] || { echo "ERROR: input not found: $IN"; exit 2; }

# ---- mmdc discovery: PATH -> managed node workspace ----
MMDC="$(command -v mmdc || true)"
[ -z "$MMDC" ] && for d in "$HOME/.workbuddy/binaries/node/workspace/node_modules/.bin" "$HOME/.workbuddy/binaries/node/versions"/*/bin; do
  [ -x "$d/mmdc" ] && MMDC="$d/mmdc" && break
done
[ -z "$MMDC" ] && { echo "ERROR: mmdc not found. Fix: npm install @mermaid-js/mermaid-cli (managed workspace)"; exit 3; }

# ---- puppeteer config: reuse local Chrome, never download Chromium ----
# 注：放在输出同目录（已存在），勿放 mktemp 目录——mmdc 对临时目录会报 EEXIST
PCFG="$(cd "$(dirname "$BASE")" && pwd)/.rnm-puppeteer-config.json"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
[ -x "$CHROME" ] || CHROME="$(command -v google-chrome || command -v chromium || echo /dev/null)"
printf '{"executablePath": "%s", "args": ["--no-sandbox", "--disable-gpu"]}\n' "$CHROME" > "$PCFG"

export PUPPETEER_SKIP_DOWNLOAD=1
OUTS=()
IFS=',' read -ra FMT_ARR <<< "$FMTS"
for fmt in "${FMT_ARR[@]}"; do
  "$MMDC" -i "$IN" -o "$BASE.$fmt" -s "$SCALE" -p "$PCFG" -b transparent >/dev/null
  OUTS+=("$BASE.$fmt")
done

for o in "${OUTS[@]}"; do [ -f "$o" ] && echo "OK: $o ($(wc -c < "$o" | tr -d ' ') bytes)"; done
rm -f "$PCFG"
