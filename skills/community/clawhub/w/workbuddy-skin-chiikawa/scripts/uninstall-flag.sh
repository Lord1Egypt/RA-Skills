#!/bin/bash
# uninstall-flag.sh — 还原 WorkBuddy 原始可执行文件
set -e
BIN="/Applications/WorkBuddy.app/Contents/MacOS/Electron"
if [ -f "$BIN.real" ]; then
  rm -f "$BIN"
  mv "$BIN.real" "$BIN"
  echo "✓ 已还原原始启动文件"
else
  echo "· 未安装过启动引子，无需还原"
fi
