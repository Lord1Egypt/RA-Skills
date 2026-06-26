#!/bin/bash
# V7守护进程 - 保持7860端口运行（强化版）
cd /home/admin/.openclaw/workspace/travel_swarm

LOG_FILE="logs/watchdog_v7.log"

while true; do
    # 检查7860端口
    if ! curl -s --connect-timeout 5 http://localhost:7860/health > /dev/null 2>&1; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') [V7守护] 7860端口未响应，重启..." >> $LOG_FILE
        
        # 杀掉旧进程
        pkill -9 -f "main_v7.py" 2>/dev/null
        sleep 2
        
        # 启动新进程（后台）
        nohup python3.8 main_v7.py >> logs/v7.log 2>&1 &
        
        # 等待启动
        sleep 8
        
        # 验证启动成功
        if curl -s http://localhost:7860/health > /dev/null 2>&1; then
            echo "$(date '+%Y-%m-%d %H:%M:%S') [V7守护] ✅ 重启成功" >> $LOG_FILE
        else
            echo "$(date '+%Y-%m-%d %H:%M:%S') [V7守护] ❌ 重启失败，等待下次检查" >> $LOG_FILE
        fi
    else
        echo "$(date '+%Y-%m-%d %H:%M:%S') [V7守护] ✅ 端口正常" >> $LOG_FILE
    fi
    
    sleep 30
done