#!/bin/bash
# 示例 2：修改 SOUL.md 后重置 - 让配置生效
# 使用场景：修改配置文件后，强制 agents 加载新配置

echo "=== Session Reset 示例：SOUL.md 更新后重置 ==="
echo ""

AGENT_NAME=${1:-"default"}

echo "修改了 SOUL.md 后，需要重置 session 才能加载新配置。"
echo ""

if [ "$AGENT_NAME" = "default" ]; then
    echo "[方式一] 重置所有 Discord sessions"
    echo "命令：openclaw session-reset --scope default --dry-run"
    openclaw session-reset --scope default --dry-run
else
    echo "[方式二] 重置指定 agent: $AGENT_NAME"
    echo "命令：openclaw session-reset --scope $AGENT_NAME --dry-run"
    openclaw session-reset --scope $AGENT_NAME --dry-run
fi

echo ""
echo "确认无误后，去掉 --dry-run 执行实际重置"
echo ""
