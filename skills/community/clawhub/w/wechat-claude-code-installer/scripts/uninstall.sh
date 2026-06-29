#!/usr/bin/env bash
# uninstall.sh —— 干净卸载
set -euo pipefail

echo "============================================================"
echo "  wechat-claude-code 干净卸载"
echo "============================================================"
echo ""
read -p "确认卸载？这会删除：" -n 1 -r
echo ""
echo "  - launchd daemon 注册"
echo "  - ~/.claude/skills/wechat-claude-code/"
echo "  - ~/.wechat-claude-code/（含账号 + sessions + 日志）"
echo ""
read -p "继续？(y/N) " confirm
if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
  echo "已取消。"
  exit 0
fi

PLIST=~/Library/LaunchAgents/com.wechat-claude-code.bridge.plist
if [ -f "$PLIST" ]; then
  echo "→ 卸载 launchd..."
  launchctl unload -w "$PLIST" 2>/dev/null || true
  rm -f "$PLIST"
fi

if [ -d ~/.claude/skills/wechat-claude-code ]; then
  echo "→ 删除上游项目..."
  rm -rf ~/.claude/skills/wechat-claude-code
fi

if [ -d ~/.wechat-claude-code ]; then
  echo "→ 删除数据目录..."
  rm -rf ~/.wechat-claude-code
fi

echo ""
echo "✅ 卸载完成。本 skill 自身仍在 ~/.claude/skills/wechat-claude-code-installer/，"
echo "   如果也想删： rm -rf ~/.claude/skills/wechat-claude-code-installer/"
