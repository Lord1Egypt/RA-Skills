#!/bin/bash
# check-status.sh - 快速检查OpenClaw状态
# 龍哥的专属状态检查 by 小包子

echo "🔍 OpenClaw 状态检查"
echo "========================"

# 1. Gateway状态
echo "🦞 Gateway状态:"
if openclaw gateway status 2>/dev/null | grep -q "Runtime: running"; then
    echo "   ✅ 运行中"
    PID=$(openclaw gateway status | grep "pid" | awk '{print $2}' | tr -d ',')
    UPTIME=$(ps -p $PID -o etime= 2>/dev/null || echo "未知")
    echo "   PID: $PID"
    echo "   运行时间: $UPTIME"
else
    echo "   ❌ 未运行"
fi

# 2. 配置文件
echo ""
echo "📁 配置文件检查:"
if [ -f ~/.openclaw/openclaw.json ]; then
    CONFIG_SIZE=$(stat -c%s ~/.openclaw/openclaw.json)
    CONFIG_AGE=$(( ($(date +%s) - $(stat -c%Y ~/.openclaw/openclaw.json)) / 60 ))
    echo "   ✅ 配置文件存在"
    echo "   大小: $((CONFIG_SIZE/1024)) KB"
    echo "   修改于: ${CONFIG_AGE}分钟前"
    
    # 检查关键配置
    if grep -q '"provider": "brave"' ~/.openclaw/openclaw.json; then
        echo "   ✅ Brave Search已配置"
    fi
else
    echo "   ❌ 配置文件缺失"
fi

# 3. 会话状态
echo ""
echo "💬 会话状态:"
SESSION_DIR="$HOME/.openclaw/agents/main/sessions"
if [ -d "$SESSION_DIR" ]; then
    SESSION_COUNT=$(find "$SESSION_DIR" -name "*.jsonl" -type f | wc -l)
    ACTIVE_SESSIONS=$(find "$SESSION_DIR" -name "*.jsonl" -type f -mmin -60 | wc -l)
    echo "   总会话数: $SESSION_COUNT"
    echo "   活跃会话(1小时内): $ACTIVE_SESSIONS"
    
    # 显示最新会话
    LATEST_SESSION=$(find "$SESSION_DIR" -name "*.jsonl" -type f -printf "%T@ %p\n" | sort -nr | head -1 | cut -d' ' -f2-)
    if [ -n "$LATEST_SESSION" ]; then
        SESSION_AGE=$(( ($(date +%s) - $(stat -c%Y "$LATEST_SESSION")) / 60 ))
        echo "   最新会话: $(basename "$LATEST_SESSION")"
        echo "   最后活动: ${SESSION_AGE}分钟前"
    fi
else
    echo "   ⚠️ 会话目录不存在"
fi

# 4. 工作空间
echo ""
echo "📂 工作空间:"
WS_DIR="$HOME/.openclaw/workspace"
if [ -d "$WS_DIR" ]; then
    echo "   ✅ 工作空间存在"
    
    # 检查记忆文件
    TODAY_FILE="$WS_DIR/memory/$(date +%Y-%m-%d).md"
    if [ -f "$TODAY_FILE" ]; then
        FILE_AGE=$(( ($(date +%s) - $(stat -c%Y "$TODAY_FILE")) / 60 ))
        echo "   今日记忆: ${FILE_AGE}分钟前更新"
    else
        echo "   ⚠️ 今日记忆文件未创建"
    fi
    
    # 检查关键文件
    for FILE in "IDENTITY.md" "USER.md" "SOUL.md"; do
        if [ -f "$WS_DIR/$FILE" ]; then
            echo "   ✅ $FILE 存在"
        else
            echo "   ⚠️ $FILE 缺失"
        fi
    done
else
    echo "   ❌ 工作空间不存在"
fi

# 5. 网络连接
echo ""
echo "🌐 网络连接:"
if curl -s --max-time 5 http://127.0.0.1:18789/ > /dev/null; then
    echo "   ✅ Gateway Web接口可访问"
else
    echo "   ❌ Gateway Web接口不可达"
fi

# 6. 重启保护状态
echo ""
echo "🛡️ 重启保护状态:"
STATE_DIR="$HOME/.openclaw/restart-state"
if [ -d "$STATE_DIR" ]; then
    # 读取配置
    MAX_HOURLY=3
    MAX_DAILY=10
    MIN_INTERVAL=300
    
    # 统计重启次数
    current_time=$(date +%s)
    hour_ago=$((current_time - 3600))
    day_ago=$((current_time - 86400))
    
    hour_restarts=0
    day_restarts=0
    last_restart=0
    
    if [ -f "$STATE_DIR/restarts.log" ]; then
        hour_restarts=$(awk -v ts="$hour_ago" '$1 > ts {count++} END {print count+0}' "$STATE_DIR/restarts.log")
        day_restarts=$(awk -v ts="$day_ago" '$1 > ts {count++} END {print count+0}' "$STATE_DIR/restarts.log")
    fi
    
    if [ -f "$STATE_DIR/last_restart" ]; then
        last_restart=$(cat "$STATE_DIR/last_restart")
        time_since_last=$((current_time - last_restart))
        if [ $time_since_last -lt 60 ]; then
            last_str="${time_since_last}秒前"
        elif [ $time_since_last -lt 3600 ]; then
            last_str="$((time_since_last/60))分钟前"
        else
            last_str="$((time_since_last/3600))小时前"
        fi
    else
        last_str="从未重启"
    fi
    
    echo "   最近1小时重启: $hour_restarts/$MAX_HOURLY 次"
    echo "   最近24小时重启: $day_restarts/$MAX_DAILY 次"
    echo "   最后重启: $last_str"
    
    # 检查限制状态
    if [ $hour_restarts -ge $MAX_HOURLY ]; then
        echo "   ⚠️ 小时限制已用尽"
    fi
    if [ $day_restarts -ge $MAX_DAILY ]; then
        echo "   ⚠️ 日限制已用尽"
    fi
else
    echo "   ⚠️ 重启状态目录未初始化"
fi

# 7. 锁文件检查
echo ""
echo "🔒 锁文件检查:"
LOCK_FILE="/tmp/openclaw-restart.lock"
if [ -f "$LOCK_FILE" ]; then
    LOCK_PID=$(cat "$LOCK_FILE" 2>/dev/null)
    if ps -p "$LOCK_PID" > /dev/null 2>&1; then
        echo "   ⚠️ 重启进程正在运行 (PID: $LOCK_PID)"
    else
        echo "   ⚠️ 发现陈旧的锁文件"
        echo "   可安全删除: rm $LOCK_FILE"
    fi
else
    echo "   ✅ 无活跃锁文件"
fi

echo ""
echo "📋 建议:"
if openclaw gateway status 2>/dev/null | grep -q "Runtime: running"; then
    echo "   ✅ 系统运行正常"
    if [ -f "$STATE_DIR/last_restart" ]; then
        last_restart=$(cat "$STATE_DIR/last_restart")
        time_since_last=$(( $(date +%s) - last_restart ))
        if [ $time_since_last -lt 300 ]; then
            wait_time=$((300 - time_since_last))
            echo "   ⏳ 距离下次重启还需等待: ${wait_time}秒"
        fi
    fi
    echo "   如需重启: ./smart-restart.sh \"重启原因\""
else
    echo "   🔧 Gateway未运行"
    echo "   请运行: openclaw gateway start"
fi

echo "========================"
echo "检查完成于: $(date '+%Y-%m-%d %H:%M:%S')"