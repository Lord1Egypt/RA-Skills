#!/usr/bin/env bash
# clip-chart.sh — reading-notes-master v2.3 图形资产管线 B4+（极客线）
# asmuth/clip：文本图表语言 .clp → SVG/PNG/PDF。适合精确控制坐标轴/时间序列/多线型的图表，
# 与 mermaid（流程图向）互补。语法参考: https://clip-lang.org 与仓库 doc/。
# 用法: clip-chart.sh <input.clp> <output.svg|png|pdf>
set -euo pipefail

[ $# -lt 2 ] && { echo "Usage: $0 <input.clp> <output.svg|png|pdf>"; exit 1; }
IN="$1"; OUT="$2"
[ -f "$IN" ] || { echo "ERROR: input not found: $IN"; exit 2; }

# ---- clip discovery: PATH -> ~/.workbuddy/bin ----
CLIP="$(command -v clip || true)"
[ -z "$CLIP" ] && [ -x "$HOME/.workbuddy/bin/clip" ] && CLIP="$HOME/.workbuddy/bin/clip"
[ -z "$CLIP" ] && { echo "ERROR: clip not found. Fix: github.com/asmuth/clip -> cmake -DCMAKE_POLICY_VERSION_MINIMUM=3.5 -> make -> cp clip ~/.workbuddy/bin/"; exit 3; }

# data 文件按 clip 官方语义相对「调用者 cwd」解析，本脚本不改变 cwd，只传绝对路径
IN_ABS="$(cd "$(dirname "$IN")" && pwd)/$(basename "$IN")"
OUT_ABS="$(cd "$(dirname "$OUT")" && pwd)/$(basename "$OUT")"
"$CLIP" -e "$OUT_ABS" "$IN_ABS" 2>&1 | grep -iE "error" && exit 4 || true
[ -f "$OUT" ] && echo "OK: $OUT ($(wc -c < "$OUT" | tr -d ' ') bytes)" || { echo "ERROR: no output"; exit 4; }
