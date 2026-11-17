#!/usr/bin/env bash
# yotta-learn error-detector —— 检测命令失败并提示记录（Linux-only）
# 用法：在 PostToolUse（Bash）hook 中指向本脚本；无输出=无错误，不打扰。
set -euo pipefail
INPUT_FILE="${1:-}"
if [ -n "$INPUT_FILE" ] && [ -f "$INPUT_FILE" ]; then
  if grep -q '"is_error": *true' "$INPUT_FILE" 2>/dev/null; then
    echo "检测到命令失败：如需沉淀经验，可运行 yotta-learn log --type error"
  fi
fi
