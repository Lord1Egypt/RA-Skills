#!/bin/bash
# 增量备份脚本 - 每5分钟运行

set -e

# 配置
BACKUP_ROOT="$HOME/.openclaw/workspace/Assets/SessionBackups"
INCREMENTAL_DIR="$BACKUP_ROOT/incremental"
LOG_FILE="$BACKUP_ROOT/backup.log"
LOCK_FILE="/tmp/session-guardian-incremental.lock"

# 创建目录
mkdir -p "$INCREMENTAL_DIR"

# 文件锁（避免并发）- macOS 兼容
if [ -f "$LOCK_FILE" ]; then
    # 检查锁文件是否超过10分钟（可能是僵尸锁）
    if [ $(find "$LOCK_FILE" -mmin +10 2>/dev/null | wc -l) -gt 0 ]; then
        rm -f "$LOCK_FILE"
    else
        echo "[$(date)] 增量备份已在运行，跳过" >> "$LOG_FILE"
        exit 0
    fi
fi

# 创建锁文件
touch "$LOCK_FILE"
trap "rm -f $LOCK_FILE" EXIT

echo "[$(date)] === 增量备份开始 ===" >> "$LOG_FILE"

# 备份计数
success_count=0
fail_count=0

# 备份所有 agent 的 sessions
for agent_dir in "$HOME/.openclaw/agents/"*/; do
    agent_name=$(basename "$agent_dir")
    sessions_dir="$agent_dir/sessions"
    
    if [ ! -d "$sessions_dir" ]; then
        continue
    fi
    
    # 使用 rsync 增量同步
    for jsonl_file in "$sessions_dir"/*.jsonl; do
        if [ ! -f "$jsonl_file" ]; then
            continue
        fi
        
        filename=$(basename "$jsonl_file")
        target="$INCREMENTAL_DIR/${agent_name}_${filename}"
        
        # rsync 增量备份（只传输变化部分）
        if rsync -a --timeout=10 "$jsonl_file" "$target" 2>/dev/null; then
            ((success_count++))
        else
            ((fail_count++))
            echo "[$(date)] 备份失败: $jsonl_file" >> "$LOG_FILE"
        fi
    done
done

# 备份 cron 任务记录
if [ -d "$HOME/.openclaw/cron/runs" ]; then
    rsync -a --timeout=10 "$HOME/.openclaw/cron/runs/"*.jsonl "$INCREMENTAL_DIR/" 2>/dev/null || true
fi

# 统计
total_size=$(du -sh "$INCREMENTAL_DIR" 2>/dev/null | cut -f1)
echo "[$(date)] 增量备份完成: 成功 $success_count, 失败 $fail_count, 总大小 $total_size" >> "$LOG_FILE"

# 健康检查
if [ $success_count -lt 3 ]; then
    echo "[$(date)] ⚠️  WARNING: 备份文件数量异常 ($success_count)" >> "$LOG_FILE"
fi
