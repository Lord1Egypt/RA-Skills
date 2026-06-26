#!/bin/bash
# 检查上下文压缩监控服务状态

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$SCRIPT_DIR/monitor.pid"
STATUS_FILE="$SCRIPT_DIR/status.json"
LOG_FILE="$SCRIPT_DIR/logs/monitor.log"

echo "=== 上下文压缩监控服务状态 ==="
echo ""

# 检查进程状态
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
        echo "✅ 服务状态: 运行中 (PID: $PID)"
        
        # 获取进程信息
        if command -v ps >/dev/null 2>&1; then
            PS_INFO=$(ps -p "$PID" -o pid,user,%cpu,%mem,etime,command 2>/dev/null | tail -n 1)
            if [ -n "$PS_INFO" ]; then
                echo "   进程信息: $PS_INFO"
            fi
        fi
    else
        echo "❌ 服务状态: 进程不存在 (PID: $PID)"
        echo "   清理PID文件..."
        rm "$PID_FILE"
    fi
else
    echo "❌ 服务状态: 未运行"
fi

echo ""

# 显示状态文件
if [ -f "$STATUS_FILE" ]; then
    echo "=== 当前状态信息 ==="
    python3 -c "
import json
import sys
from datetime import datetime

try:
    with open('$STATUS_FILE', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 格式化输出
    print(f\"检查时间: {data.get('timestamp', '未知')}\")
    
    stats = data.get('stats', {})
    print(f\"总检查次数: {stats.get('total_checks', 0)}\")
    print(f\"总压缩触发: {stats.get('total_compactions_triggered', 0)}\")
    
    usage = data.get('current_usage', {})
    print(f\"当前Token使用率: {usage.get('token_usage', 0):.2%}\")
    print(f\"当前消息数量: {usage.get('message_count', 0)}\")
    
    config = data.get('config', {})
    print(f\"检查间隔: {config.get('check_interval', 30)}秒\")
    print(f\"Token阈值: {config.get('token_usage_threshold', 0.7):.2%}\")
    print(f\"消息阈值: {config.get('message_count_threshold', 50)}\")
    
except Exception as e:
    print(f\"读取状态文件失败: {e}\")
"
else
    echo "状态文件不存在"
fi

echo ""

# 显示最新日志
if [ -f "$LOG_FILE" ]; then
    echo "=== 最新日志 (最后10行) ==="
    tail -n 10 "$LOG_FILE"
else
    echo "日志文件不存在"
fi

echo ""

# 显示数据库状态
DB_FILE="$SCRIPT_DIR/context_compactor.db"
if [ -f "$DB_FILE" ]; then
    echo "=== 数据库状态 ==="
    python3 -c "
import sqlite3
import json
import sys

try:
    conn = sqlite3.connect('$DB_FILE')
    cursor = conn.cursor()
    
    # 压缩历史
    cursor.execute('SELECT COUNT(*) FROM compaction_history')
    history_count = cursor.fetchone()[0]
    print(f\"压缩历史记录: {history_count} 条\")
    
    if history_count > 0:
        cursor.execute('''
            SELECT 
                COUNT(*) as total,
                SUM(tokens_before - tokens_after) as total_saved,
                AVG(compression_ratio) as avg_ratio
            FROM compaction_history
        ''')
        row = cursor.fetchone()
        print(f\"总节省Token: {row[1] or 0}\")
        print(f\"平均压缩率: {(row[2] or 0):.2%}\")
    
    # 分层数据
    cursor.execute('SELECT COUNT(*) FROM tiered_data')
    tiered_count = cursor.fetchone()[0]
    print(f\"分层数据记录: {tiered_count} 条\")
    
    if tiered_count > 0:
        cursor.execute('''
            SELECT layer, COUNT(*), AVG(importance_score)
            FROM tiered_data 
            GROUP BY layer
        ''')
        print(\"分层统计:\")
        for layer, count, avg_importance in cursor.fetchall():
            print(f\"  {layer}: {count} 条 (平均重要性: {avg_importance:.2f})\")
    
    conn.close()
    
except Exception as e:
    print(f\"读取数据库失败: {e}\")
"
else
    echo "数据库文件不存在"
fi