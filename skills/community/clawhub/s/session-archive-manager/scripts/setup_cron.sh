#!/bin/bash

# 设置定时任务来自动运行 session 归档脚本

SCRIPT_PATH="/root/.openclaw/workspace/archive_sessions.sh"
CRON_LOG="/root/.openclaw/workspace/archive_sessions.log"
CRON_JOB="0 * * * * $SCRIPT_PATH >> $CRON_LOG 2>&1"

echo "=== 设置 Session 归档定时任务 ==="
echo ""

# 检查脚本是否存在
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "错误: 找不到脚本 $SCRIPT_PATH"
    exit 1
fi

# 确保脚本有执行权限
chmod +x "$SCRIPT_PATH"

# 创建日志文件
touch "$CRON_LOG"

echo "脚本路径: $SCRIPT_PATH"
echo "日志文件: $CRON_LOG"
echo ""

# 检查当前的 cron 任务
echo "当前的 cron 任务:"
crontab -l 2>/dev/null || echo "(暂无定时任务)"
echo ""

# 检查是否已经存在相同的任务
if crontab -l 2>/dev/null | grep -q "$SCRIPT_PATH"; then
    echo "定时任务已存在，正在更新..."
    # 删除旧任务
    (crontab -l 2>/dev/null | grep -v "$SCRIPT_PATH"; echo "$CRON_JOB") | crontab -
else
    echo "添加新的定时任务..."
    # 添加新任务
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
fi

echo ""
echo "=== 完成 ==="
echo "定时任务已设置为每小时运行一次"
echo "可以使用 'crontab -l' 查看当前任务"
echo "可以使用 'tail -f $CRON_LOG' 查看日志"
