#!/bin/bash
# 示例 1：日常维护 - 清理过期 Discord sessions
# 使用场景：定期清理，保持系统整洁

echo "=== Session Reset 示例：日常维护 ==="
echo ""

# 步骤 1：预览将要清理的内容
echo "[步骤 1] 预览将要重置的 sessions..."
openclaw session-reset --scope default --dry-run

echo ""
echo "[步骤 2] 确认无误后执行重置"
echo "执行命令：openclaw session-reset --scope default"
echo ""

# 实际执行（取消注释以运行）
# openclaw session-reset --scope default

echo "[步骤 3] 清理旧备份"
echo "执行命令：openclaw session-reset --cleanup"
echo ""

# 实际执行（取消注释以运行）
# openclaw session-reset --cleanup
