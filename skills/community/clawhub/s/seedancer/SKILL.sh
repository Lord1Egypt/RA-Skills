#!/usr/bin/env bash
# Seedancer — 硬门计算器 + 提示词模板助手
#
# 用法：
#   ./SKILL.sh "你的视频描述"                     # 模板输出（向后兼容）
#   ./SKILL.sh smin 12 ordinary                   # 镜头数硬下限 Smin / Gmax
#   ./SKILL.sh dialogue "台词" --pace slow          # 台词最低时长
#   ./SKILL.sh check-group --model seedance-2.0 --duration 12 --type ordinary \
#       --shots 5 --line "台词一" --line "台词二"     # 一组分镜三道硬门
#   ./SKILL.sh models                             # 各模型分组时长上限
#   ./SKILL.sh --help
#
# 计算类子命令委托给 scripts/seedancer_calc.py（零依赖，需 python3）。
# 完整工作流见 SKILL.md 与 references/INDEX.md。

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CALC="$HERE/scripts/seedancer_calc.py"

usage() {
  sed -n '2,13p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
}

case "${1:-}" in
  -h|--help|help)
    usage
    exit 0
    ;;
  smin|dialogue|check-group|models)
    if ! command -v python3 >/dev/null 2>&1; then
      echo "需要 python3 才能运行计算类子命令" >&2
      exit 2
    fi
    exec python3 "$CALC" "$@"
    ;;
esac

REQ="${1:-10s 9:16 cinematic prompt using @image1 as first frame}"

# 从请求中提取时长与画幅（提取不到时用默认值，并如实标注）
DUR="$(printf '%s' "$REQ" | grep -oE '[0-9]+ ?(s|秒)' | head -n1 | grep -oE '[0-9]+' || true)"
RATIO="$(printf '%s' "$REQ" | grep -oE '(16:9|9:16|1:1|4:3|3:4|21:9|2\.39:1)' | head -n1 || true)"
DUR_NOTE=""; RATIO_NOTE=""
if [ -z "$DUR" ]; then DUR=10; DUR_NOTE="（未指定，默认）"; fi
if [ -z "$RATIO" ]; then RATIO="16:9"; RATIO_NOTE="（未指定，默认）"; fi

# 三段式时间片：0–a / a–b / b–DUR（整数秒，连续不重叠）
A=$(( DUR * 3 / 10 )); [ "$A" -lt 1 ] && A=1
B=$(( DUR * 7 / 10 )); [ "$B" -le "$A" ] && B=$(( A + 1 ))
[ "$B" -ge "$DUR" ] && B=$(( DUR - 1 ))

echo "Seedancer Prompt Helper (Basic Template)"
echo "Request: $REQ"
echo "Duration: ${DUR}s${DUR_NOTE}   Aspect ratio: ${RATIO}${RATIO_NOTE}"
echo ""
if [ "$DUR" -gt 15 ]; then
  echo "⚠️  ${DUR}s 超过 Seedance 2.0 / Kling 3.0 的 15s 分组上限，需拆组或改用支持更长时长的模型。"
  echo "   运行 ./SKILL.sh models 查看各模型上限。"
  echo ""
fi
cat <<EOF
---
Mode: Basic Template (完整功能请加载 SKILL.md)
Assets Mapping:
- @image1: first frame reference (optional)
- @video1: camera reference (optional)

Basic Prompt Structure:
[aspect_ratio], [duration], [style], [scene], [action], [camera]

Example:
${RATIO}, ${DUR}s, cinematic, physically plausible motion.
0-${A}s: setup shot + subject intro.
${A}-${B}s: core action + controlled camera movement.
${B}-${DUR}s: climax/reveal + clean, stable landing frame.

Negative Constraints:
no watermark, no logo, no subtitles, no on-screen text.
---
EOF

echo ""
echo "Next: ./SKILL.sh smin ${DUR} ordinary   # 本组至少需要几个编号镜头"
echo "⚠️  This is a basic template. For the full pipeline, load SKILL.md in your agent."
