#!/bin/bash
# 示例 5：高级用法 - 自定义清理策略
# 使用场景：自定义备份保留策略

echo "=== Session Reset 示例：高级用法 ==="
echo ""

echo "[示例 5.1] 自定义清理策略 - 保留7天，最多5个备份"
echo "命令：openclaw session-reset --cleanup --cleanup-days 7 --cleanup-max 5"
echo ""

# 实际执行（取消注释以运行）
# openclaw session-reset --cleanup --cleanup-days 7 --cleanup-max 5

echo ""
echo "[示例 5.2] 强制执行（跳过确认）- 谨慎使用！"
echo "命令：openclaw session-reset --scope default --force"
echo ""

echo "[示例 5.3] 重置特定 agents 列表"
echo "命令：openclaw session-reset --scope main,hubu,libu --dry-run"
openclaw session-reset --scope main,hubu,libu --dry-run
