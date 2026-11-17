#!/usr/bin/env bash
# yotta-learn activator —— 会话开始时提醒 review 学习条目（Linux-only）
# 用法：在 hook 配置中指向本脚本；脚本定位技能目录后调用 CLI。
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if command -v python3 >/dev/null 2>&1; then
  python3 "$SKILL_DIR/scripts/yotta_learn.py" review 2>/dev/null || true
fi
