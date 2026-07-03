#!/bin/bash
# todos/scripts/cron_setup.sh
# 配置 todo-list 定时提醒
# 用法：./scripts/cron_setup.sh
# 版本：v1.0 | 日期：2026-06-11

# === 路径配置 ===
TODOS_DIR="/home/qwenpaw/.qwenpaw/workspaces/default/todos"
TODOS_DB="$TODOS_DIR/todos.db"

# === Cron 任务 ===
CRON_DAILY_DUE="0 9 * * * cd $TODOS_DIR && python3 -m src.reminder daily-due --push >> $TODOS_DIR/logs/reminder.log 2>&1"
CRON_CHECK_OVERDUE="5 0 * * * cd $TODOS_DIR && python3 -m src.reminder check-overdue >> $TODOS_DIR/logs/reminder.log 2>&1"
CRON_ARCHIVE="0 3 1 * * cd $TODOS_DIR && python3 -m src.reminder archive-cleanup >> $TODOS_DIR/logs/reminder.log 2>&1"

# === 创建日志目录 ===
mkdir -p $TODOS_DIR/logs

# === 安装 cron 任务 ===
(crontab -l 2>/dev/null | grep -v "src.reminder"; echo "$CRON_DAILY_DUE"; echo "$CRON_CHECK_OVERDUE"; echo "$CRON_ARCHIVE") | crontab -

echo "✅ Cron 任务已安装："
echo "  - 每天 09:00 推送当天到期"
echo "  - 每天 00:05 标记过期"
echo "  - 每月 1 号 03:00 清理 archive"
echo ""
echo "查看：crontab -l"
echo "移除：crontab -e（删除含 src.reminder 的行）"