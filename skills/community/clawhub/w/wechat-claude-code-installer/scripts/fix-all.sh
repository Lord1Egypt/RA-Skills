#!/usr/bin/env bash
# fix-all.sh —— 一次跑完 1+2+3
set -euo pipefail

WORK_DIR="${1:-$HOME/Claude Code}"
DIR="$(dirname "$0")"

echo "============================================================"
echo "  fix-all :: 一次修复所有已知坑"
echo "============================================================"
echo ""

bash "$DIR/fix-cwd.sh" "$WORK_DIR"
echo ""
bash "$DIR/fix-meta-talk.sh"
echo ""
bash "$DIR/fix-caffeinate.sh"

echo ""
echo "============================================================"
echo "  ✅ 全部修复完成。在微信里给 AI bot 发任意消息测试。"
echo "============================================================"
