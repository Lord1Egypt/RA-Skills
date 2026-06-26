#!/bin/bash

# 🦞 三只虾心跳检查脚本
# 工作时间 8:00-18:00，每小时执行一次
# 飞书 COO（阿虾）专用 - 统筹终端虾和 Telegram 虾

set -e

WORKSPACE="/Users/zhangyang/.openclaw/workspace"
QUEUE_FILE="$WORKSPACE/tasks/queue.md"
MEMORY_FILE="$WORKSPACE/MEMORY.md"
DIVISION_FILE="$WORKSPACE/三只虾分工体系.md"
COLLAB_FILE="$WORKSPACE/三只虾协同协议.md"
LOG_DIR="$WORKSPACE/logs"

# 创建日志目录
mkdir -p "$LOG_DIR"

# 获取当前时间
CURRENT_HOUR=$(date +%H)
CURRENT_TIME=$(date +"%Y-%m-%d %H:%M")
LOG_FILE="$LOG_DIR/heartbeat-$(date +%Y-%m-%d).log"

# 日志函数
log() {
    echo "[$CURRENT_TIME] $1" | tee -a "$LOG_FILE"
}

# 检查是否在工作时间（8:00-18:00）
if [ "$CURRENT_HOUR" -lt 8 ] || [ "$CURRENT_HOUR" -ge 18 ]; then
    log "⏰ 非工作时间，跳过心跳检查"
    exit 0
fi

log "🦞 开始心跳检查 - $CURRENT_TIME"
log "================================"

# Layer 1: 快速检查任务队列
if [ -f "$QUEUE_FILE" ]; then
    log "📋 检查任务队列..."
    
    # 检查是否有待处理任务
    PENDING_TASKS=$(grep -c "^\- \[ \]" "$QUEUE_FILE" 2>/dev/null || echo "0")
    log "  待处理任务：$PENDING_TASKS"
    
    # 检查是否有处理中任务
    PROCESSING_TASKS=$(grep -c "^\- \[~\]" "$QUEUE_FILE" 2>/dev/null || echo "0")
    log "  处理中任务：$PROCESSING_TASKS"
    
    # 检查是否有已完成任务（今天）
    COMPLETED_TODAY=$(grep "^\- \[x\]" "$QUEUE_FILE" 2>/dev/null | grep -c "$(date +%Y-%m-%d)" || echo "0")
    log "  今日已完成：$COMPLETED_TODAY"
    
    # 按角色统计
    log "  按角色统计:"
    CPMO_PENDING=$(grep "^\- \[ \] \[CPMO\]" "$QUEUE_FILE" 2>/dev/null | wc -l | tr -d ' ')
    COO_PENDING=$(grep "^\- \[ \] \[COO\]" "$QUEUE_FILE" 2>/dev/null | wc -l | tr -d ' ')
    CGO_PENDING=$(grep "^\- \[ \] \[CGO\]" "$QUEUE_FILE" 2>/dev/null | wc -l | tr -d ' ')
    log "    [CPMO] 终端虾待处理：$CPMO_PENDING"
    log "    [COO] 飞书虾待处理：$COO_PENDING"
    log "    [CGO] Telegram 虾待处理：$CGO_PENDING"
    
    if [ "$PENDING_TASKS" -gt 0 ]; then
        log "  ✅ 有待处理任务，需要执行"
        
        # 检查是否有分配给 COO 的任务
        if [ "$COO_PENDING" -gt 0 ]; then
            log "  📊 有分配给 COO（我）的任务，准备执行"
        fi
        
        # 检查是否有分配给 CGO 的任务（需要统筹）
        if [ "$CGO_PENDING" -gt 0 ]; then
            log "  ⚡ 有分配给 CGO（Telegram 虾）的任务，需要统筹跟进"
        fi
        
        # 检查是否有分配给 CPMO 的任务（需要协管）
        if [ "$CPMO_PENDING" -gt 0 ]; then
            log "  🦞 有分配给 CPMO（终端虾）的任务，需要协管"
        fi
    else
        log "  ✅ 无待处理任务"
    fi
else
    log "  ⚠️ 任务队列文件不存在"
fi

# Layer 2: 完整同步（每天 12:00）
if [ "$CURRENT_HOUR" -eq 12 ]; then
    log "🔄 执行完整同步..."
    
    FILES_TO_CHECK=(
        "$MEMORY_FILE:长期记忆"
        "$DIVISION_FILE:分工体系"
        "$COLLAB_FILE:协同协议"
        "$QUEUE_FILE:任务队列"
    )
    
    for file_desc in "${FILES_TO_CHECK[@]}"; do
        FILE=$(echo "$file_desc" | cut -d: -f1)
        DESC=$(echo "$file_desc" | cut -d: -f2)
        if [ -f "$FILE" ]; then
            SIZE=$(wc -c < "$FILE" | tr -d ' ')
            log "  ✅ $DESC 存在 ($SIZE bytes)"
        else
            log "  ⚠️ $DESC 不存在"
        fi
    done
    
    # 检查 Telegram 虾配置
    TG_FILE="$WORKSPACE/channels/telegram.md"
    if [ -f "$TG_FILE" ]; then
        log "  ✅ Telegram 虾配置存在"
        # 提取 CGO 职责
        log "  📋 Telegram 虾（CGO）职责:"
        grep -A 5 "职责范围" "$TG_FILE" 2>/dev/null | head -6 | while read line; do
            log "    $line"
        done
    else
        log "  ⚠️ Telegram 虾配置不存在"
    fi
    
    # 检查终端虾配置
    WEBCHAT_FILE="$WORKSPACE/channels/webchat.md"
    if [ -f "$WEBCHAT_FILE" ]; then
        log "  ✅ 终端虾配置存在"
    else
        log "  ⚠️ 终端虾配置不存在"
    fi
fi

# Layer 3: 每日总结（每天 17:00）
if [ "$CURRENT_HOUR" -eq 17 ]; then
    log "📊 执行每日总结..."
    
    # 统计今日任务
    log "  今日任务统计:"
    TODAY=$(date +%Y-%m-%d)
    COMPLETED=$(grep "^\- \[x\]" "$QUEUE_FILE" 2>/dev/null | grep -c "$TODAY" || echo "0")
    log "    已完成：$COMPLETED"
    
    # 生成简报（可以发送到飞书）
    log "  📝 生成每日协同简报..."
    # 这里可以添加发送飞书消息的逻辑
fi

# Layer 4: 检测新完成的任务并通知
log "🔍 检测新完成的任务..."
LAST_CHECK_FILE="$LOG_DIR/.last_check_$(date +%Y-%m-%d).txt"

if [ -f "$LAST_CHECK_FILE" ]; then
    LAST_COMPLETED=$(cat "$LAST_CHECK_FILE" | sort)
    CURRENT_COMPLETED=$(grep "^\- \[x\]" "$QUEUE_FILE" 2>/dev/null | sort)
    
    # 找出新完成的任务
    NEW_TASKS=$(comm -13 <(echo "$LAST_COMPLETED") <(echo "$CURRENT_COMPLETED") 2>/dev/null || echo "")
    
    if [ -n "$NEW_TASKS" ]; then
        log "✅ 发现新完成的任务:"
        echo "$NEW_TASKS" | while read task; do
            if [ -n "$task" ]; then
                # 提取任务信息
                TASK_NAME=$(echo "$task" | sed 's/^- \[x\] //' | cut -d' - ' -f2-)
                log "  - $TASK_NAME"
                
                # 生成通知消息
                NOTIFICATION="✅ 任务完成通知

📋 任务：$TASK_NAME
🦞 执行者：自动检测
⏰ 完成时间：$CURRENT_TIME

---
_三只虾协同系统自动通知_"
                
                # 保存到通知文件（供飞书虾读取并发送）
                echo "$NOTIFICATION" >> "$LOG_DIR/pending-notifications-$(date +%Y-%m-%d).md"
                log "  📱 已生成通知消息"
            fi
        done
    else
        log "ℹ️  无新完成任务"
    fi
else
    log "ℹ️  首次检查，建立基线..."
    grep "^\- \[x\]" "$QUEUE_FILE" 2>/dev/null | sort > "$LAST_CHECK_FILE"
fi

# 更新检查记录
grep "^\- \[x\]" "$QUEUE_FILE" 2>/dev/null | sort > "$LAST_CHECK_FILE"

log "✅ 心跳检查完成"
log ""

# 返回状态
if [ "$PENDING_TASKS" -gt 0 ]; then
    exit 1  # 有待处理任务
else
    exit 0  # 无任务
fi
