#!/bin/bash
# 每小时快照脚本

set -e

# 配置
BACKUP_ROOT="$HOME/.openclaw/workspace/Assets/SessionBackups"
HOURLY_DIR="$BACKUP_ROOT/hourly"
LOG_FILE="$BACKUP_ROOT/backup.log"
TIMESTAMP=$(date +%Y-%m-%d-%H)
SNAPSHOT_DIR="$HOURLY_DIR/$TIMESTAMP"

# 创建目录
mkdir -p "$SNAPSHOT_DIR"

echo "[$(date)] === 快照备份开始: $TIMESTAMP ===" >> "$LOG_FILE"

# 完整备份所有 sessions
for agent_dir in "$HOME/.openclaw/agents/"*/; do
    agent_name=$(basename "$agent_dir")
    sessions_dir="$agent_dir/sessions"
    
    if [ ! -d "$sessions_dir" ]; then
        continue
    fi
    
    # 创建 agent 子目录
    mkdir -p "$SNAPSHOT_DIR/$agent_name"
    
    # 复制所有 .jsonl 文件
    cp "$sessions_dir"/*.jsonl "$SNAPSHOT_DIR/$agent_name/" 2>/dev/null || true
done

# 备份 cron 任务
if [ -d "$HOME/.openclaw/cron/runs" ]; then
    mkdir -p "$SNAPSHOT_DIR/cron"
    cp "$HOME/.openclaw/cron/runs"/*.jsonl "$SNAPSHOT_DIR/cron/" 2>/dev/null || true
fi

# 压缩快照
cd "$HOURLY_DIR"
tar -czf "$TIMESTAMP.tar.gz" "$TIMESTAMP/" 2>/dev/null || true
rm -rf "$TIMESTAMP/"

# 统计
snapshot_size=$(du -sh "$TIMESTAMP.tar.gz" 2>/dev/null | cut -f1)
echo "[$(date)] 快照备份完成: $TIMESTAMP.tar.gz ($snapshot_size)" >> "$LOG_FILE"

# 清理超过24小时的快照
find "$HOURLY_DIR" -name "*.tar.gz" -mmin +1440 -delete 2>/dev/null || true

echo "[$(date)] 快照清理完成" >> "$LOG_FILE"
