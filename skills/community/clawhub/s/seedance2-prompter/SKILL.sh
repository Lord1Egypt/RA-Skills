#!/usr/bin/env bash
# Seedance 2.0 即梦 — 提示词工程测试脚本
# 用法：
#   ./SKILL.sh "你的需求"
# 示例：
#   ./SKILL.sh "10s 9:16 奇幻揭示 使用 @image1 和 @video1"

set -euo pipefail

REQ="${1:-10s 9:16 cinematic prompt using @image1 as first frame and @video1 as camera reference}"

echo "Seedance 2.0 提示词工程"
echo "需求: $REQ"
echo ""
echo "模板输出:"
cat <<'EOF'
Mode: All-Reference
Assets Mapping:
- @image1: first frame / character identity anchor
- @video1: camera language + motion rhythm
- @audio1: optional rhythm reference

Final Prompt:
9:16, 10s, cinematic, physically plausible motion.
0-3s: setup shot + subject intro.
3-7s: core action + controlled camera movement.
7-10s: climax/reveal + clean landing frame.

Negative Constraints:
no watermark, no logo, no subtitles, no on-screen text.
EOF
