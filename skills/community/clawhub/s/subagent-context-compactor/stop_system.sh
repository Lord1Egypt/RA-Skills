#!/bin/bash
# 停止上下文压缩系统

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SYSTEM_PID_FILE="$SCRIPT_DIR/system.pid"
MONITOR_PID_FILE="$SCRIPT_DIR/monitor.pid"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

echo "=" | tr "=" "="
echo "   停止上下文压缩系统"
echo "=" | tr "=" "="
echo ""

# 1. 停止集成服务
if [ -f "$SYSTEM_PID_FILE" ]; then
    SYSTEM_PID=$(cat "$SYSTEM_PID_FILE")
    
    if kill -0 "$SYSTEM_PID" 2>/dev/null; then
        log_info "停止集成服务 (PID: $SYSTEM_PID)..."
        kill -TERM "$SYSTEM_PID"
        
        # 等待进程结束
        for i in {1..10}; do
            if ! kill -0 "$SYSTEM_PID" 2>/dev/null; then
                log_success "集成服务已停止"
                rm "$SYSTEM_PID_FILE"
                break
            fi
            sleep 1
        done
        
        # 检查是否停止
        if kill -0 "$SYSTEM_PID" 2>/dev/null; then
            log_warning "进程未响应，强制停止..."
            kill -KILL "$SYSTEM_PID"
            sleep 2
            
            if ! kill -0 "$SYSTEM_PID" 2>/dev/null; then
                log_success "集成服务已强制停止"
                rm "$SYSTEM_PID_FILE"
            else
                log_error "无法停止集成服务进程"
                exit 1
            fi
        fi
    else
        log_warning "集成服务进程不存在，清理PID文件..."
        rm "$SYSTEM_PID_FILE"
    fi
else
    log_warning "集成服务PID文件不存在"
fi

# 2. 停止监控服务
if [ -f "$MONITOR_PID_FILE" ]; then
    MONITOR_PID=$(cat "$MONITOR_PID_FILE")
    
    if kill -0 "$MONITOR_PID" 2>/dev/null; then
        log_info "停止监控服务 (PID: $MONITOR_PID)..."
        kill -TERM "$MONITOR_PID"
        
        # 等待进程结束
        for i in {1..5}; do
            if ! kill -0 "$MONITOR_PID" 2>/dev/null; then
                log_success "监控服务已停止"
                rm "$MONITOR_PID_FILE"
                break
            fi
            sleep 1
        done
        
        # 检查是否停止
        if kill -0 "$MONITOR_PID" 2>/dev/null; then
            log_warning "监控服务进程未响应，强制停止..."
            kill -KILL "$MONITOR_PID"
            sleep 1
            
            if ! kill -0 "$MONITOR_PID" 2>/dev/null; then
                log_success "监控服务已强制停止"
                rm "$MONITOR_PID_FILE"
            fi
        fi
    else
        log_warning "监控服务进程不存在，清理PID文件..."
        rm "$MONITOR_PID_FILE"
    fi
fi

# 3. 检查是否有其他相关进程
log_info "检查其他相关进程..."
PYTHON_PROCESSES=$(pgrep -f "python3.*(monitor|integration|hierarchical_compactor)" || true)

if [ -n "$PYTHON_PROCESSES" ]; then
    log_warning "发现其他Python进程，正在停止..."
    echo "$PYTHON_PROCESSES" | xargs kill -TERM 2>/dev/null || true
    sleep 2
    
    # 检查是否还有进程
    REMAINING_PROCESSES=$(pgrep -f "python3.*(monitor|integration|hierarchical_compactor)" || true)
    if [ -n "$REMAINING_PROCESSES" ]; then
        log_warning "强制停止剩余进程..."
        echo "$REMAINING_PROCESSES" | xargs kill -KILL 2>/dev/null || true
    fi
fi

# 4. 显示停止状态
echo ""
log_info "系统状态检查:"

# 检查集成服务
if [ -f "$SYSTEM_PID_FILE" ]; then
    log_error "集成服务PID文件仍然存在"
else
    log_success "集成服务已停止"
fi

# 检查监控服务
if [ -f "$MONITOR_PID_FILE" ]; then
    log_error "监控服务PID文件仍然存在"
else
    log_success "监控服务已停止"
fi

# 检查进程
REMAINING=$(pgrep -f "python3.*(monitor|integration|hierarchical_compactor)" | wc -l)
if [ "$REMAINING" -gt 0 ]; then
    log_error "仍有 $REMAINING 个相关进程在运行"
else
    log_success "所有相关进程已停止"
fi

# 5. 显示最终报告
echo ""
log_info "最终报告:"

# 数据库状态
DB_FILE="$SCRIPT_DIR/context_compactor.db"
if [ -f "$DB_FILE" ]; then
    DB_SIZE=$(du -h "$DB_FILE" | cut -f1)
    log_info "  数据库大小: $DB_SIZE"
    
    # 显示压缩统计
    if command -v python3 >/dev/null 2>&1; then
        python3 -c "
import sqlite3
import json
import sys

try:
    conn = sqlite3.connect('$DB_FILE')
    cursor = conn.cursor()
    
    # 压缩历史
    cursor.execute('SELECT COUNT(*), SUM(tokens_before - tokens_after) FROM compaction_history')
    row = cursor.fetchone()
    count, total_saved = row
    
    if count and count > 0:
        print(f'  总压缩次数: {count}')
        print(f'  总节省Token: {total_saved or 0}')
    else:
        print('  无压缩历史记录')
    
    # 分层数据
    cursor.execute('SELECT tier, COUNT(*) FROM tiered_data GROUP BY tier')
    tiers = cursor.fetchall()
    
    if tiers:
        print('  分层数据统计:')
        for tier, count in tiers:
            print(f'    {tier}: {count} 条')
    
    conn.close()
    
except Exception as e:
    print(f'  读取数据库失败: {e}')
"
    fi
else
    log_warning "  数据库文件不存在"
fi

# 日志文件
LOG_DIR="$SCRIPT_DIR/logs"
if [ -d "$LOG_DIR" ]; then
    LOG_COUNT=$(find "$LOG_DIR" -name "*.log" | wc -l)
    LOG_SIZE=$(du -sh "$LOG_DIR" | cut -f1)
    log_info "  日志文件: $LOG_COUNT 个 ($LOG_SIZE)"
fi

echo ""
log_success "上下文压缩系统已完全停止"
echo ""
echo "可以使用 start_system.sh 重新启动系统。"