#!/bin/bash
# screen-reviewer 卸载脚本
set -e

DATA_DIR="$HOME/.screen-reviewer"
CURSOR_SKILL="$HOME/.cursor/skills/screen-reviewer"
CODEX_SKILL="$HOME/.codex/skills/screen-reviewer"

echo "正在卸载 screen-reviewer..."

# 停止守护进程
if [ -f "$DATA_DIR/.capture.pid" ]; then
    PID=$(cat "$DATA_DIR/.capture.pid")
    kill "$PID" 2>/dev/null && echo "  已停止守护进程 (PID=$PID)" || true
fi

# 卸载 launchd 服务
for label in com.screen-reviewer.capture com.screen-reviewer.report; do
    PLIST="$HOME/Library/LaunchAgents/$label.plist"
    if [ -f "$PLIST" ]; then
        launchctl unload "$PLIST" 2>/dev/null || true
        rm -f "$PLIST"
        echo "  已移除 launchd: $label"
    fi
done

# 移除 skill symlink
rm -f "$CURSOR_SKILL" && echo "  已移除 Cursor Skill"
rm -f "$CODEX_SKILL" && echo "  已移除 Codex Skill"

echo ""
echo "✅ 卸载完成"
echo ""
echo "以下数据已保留（含你的日志和报告），如需彻底删除请手动执行:"
echo "  rm -rf $DATA_DIR"
