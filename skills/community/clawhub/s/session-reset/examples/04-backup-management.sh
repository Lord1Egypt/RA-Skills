#!/bin/bash
# 示例 4：备份管理 - 查看和恢复
# 使用场景：误删 sessions 后的恢复

echo "=== Session Reset 示例：备份管理 ==="
echo ""

# 查看所有备份
echo "[步骤 1] 查看所有可用备份"
openclaw session-reset --list-backups

echo ""
echo "[步骤 2] 恢复到指定备份点"
echo "用法：openclaw session-reset --restore <时间戳>"
echo ""
echo "示例："
echo "  openclaw session-reset --restore 20250305_143022"
echo ""

# 如果有参数传入，执行恢复
if [ -n "$1" ]; then
    echo "正在恢复到备份: $1"
    openclaw session-reset --restore "$1"
fi
