#!/bin/bash
# Cron 触发脚本
# 每日 00:00 自动触发，遍历所有 agent

set -e

# 获取脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 获取共享学习目录
SHARED_LEARNING_DIR="${SHARED_LEARNING_DIR:-/root/.openclaw/shared-learning}"

# 日志文件
LOG_FILE="$SCRIPT_DIR/../logs/heartbeat-daily.log"

# 状态文件
STATE_FILE="$SCRIPT_DIR/../heartbeat-state.json"

# 确保日志目录存在
mkdir -p "$(dirname "$LOG_FILE")"

# 记录执行
echo "=== Self-Evolution-CN Daily Review (All Agents): $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG_FILE"

# 获取所有 agent 列表
WORKSPACE_BASE="/root/.openclaw"
AGENTS=()

# 获取 agent ID 和 workspace 的对应关系
declare -A AGENT_WORKSPACES
if command -v openclaw &> /dev/null; then
    # 使用 OpenClaw 配置 API 获取 agent 列表
    while IFS= read -r line; do
        if [[ $line =~ ^([a-zA-Z0-9_-]+)\ -\>\ (.+)$ ]]; then
            agent_id="${BASH_REMATCH[1]}"
            workspace="${BASH_REMATCH[2]}"
            AGENTS+=("$agent_id")
            AGENT_WORKSPACES["$agent_id"]="$workspace"
        fi
    done < <(openclaw config get agents.list 2>&1 | jq -r '.[] | "\(.id) -> \(.workspace)"' 2>/dev/null)
fi

# 如果没有找到 agent，使用默认值
if [ ${#AGENTS[@]} -eq 0 ]; then
    AGENTS=("agent1")
    AGENT_WORKSPACES["agent1"]="$WORKSPACE_BASE/workspace-agent1"
fi

echo "找到 ${#AGENTS[@]} 个 agent: ${AGENTS[*]}" >> "$LOG_FILE"

# 遍历所有 agent
for AGENT_ID in "${AGENTS[@]}"; do
    echo "" >> "$LOG_FILE"
    echo "--- Processing agent: $AGENT_ID ---" >> "$LOG_FILE"

    # 检查今日是否已执行
    if [ -f "$STATE_FILE" ]; then
        LAST_DATE=$(cat "$STATE_FILE" | grep -o "\"$AGENT_ID\".*\"last_execution_date\":\"[^\"]*\"" | grep -o '"last_execution_date":"[^"]*"' | cut -d'"' -f4 | head -1)
        TODAY=$(date '+%Y-%m-%d')

        if [ "$LAST_DATE" = "$TODAY" ]; then
            echo "今日已执行日检查（$TODAY），跳过。" >> "$LOG_FILE"
            continue
        fi
    fi

    # 运行日检查脚本
    echo "执行日检查..." >> "$LOG_FILE"
    AGENT_ID="$AGENT_ID" bash "$SCRIPT_DIR/daily_review.sh" >> "$LOG_FILE" 2>&1

    # 更新状态文件
    # 如果状态文件不存在，创建空结构
    if [ ! -f "$STATE_FILE" ]; then
        echo '{"agents":{}}' > "$STATE_FILE"
    fi

    # 更新当前 agent 的状态
    CURRENT_TIME=$(date '+%Y-%m-%dT%H:%M:%S%:z')
    TODAY=$(date '+%Y-%m-%d')

    # 使用 jq 更新状态文件（如果可用），否则使用 sed
    if command -v jq &> /dev/null; then
        jq --arg agent "$AGENT_ID" --arg date "$TODAY" --arg time "$CURRENT_TIME" \
            '.agents[$agent] = {
                "last_execution_date": $date,
                "last_execution_time": $time,
                "status": "completed"
            }' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
    else
        # 使用 sed 更新（简单实现）
        # 注意：这不是完美的 JSON 更新，但足够用于基本用途
        sed -i "s/\"$AGENT_ID\":{[^}]*}/\"$AGENT_ID\":{\"last_execution_date\":\"$TODAY\",\"last_execution_time\":\"$CURRENT_TIME\",\"status\":\"completed\"}/g" "$STATE_FILE"
        # 如果 agent 不存在，添加它
        if ! grep -q "\"$AGENT_ID\":" "$STATE_FILE"; then
            sed -i "s/{/{\"$AGENT_ID\":{\"last_execution_date\":\"$TODAY\",\"last_execution_time\":\"$CURRENT_TIME\",\"status\":\"completed\"},/" "$STATE_FILE"
        fi
    fi

    echo "状态已更新：agent = $AGENT_ID, last_execution_date = $TODAY" >> "$LOG_FILE"
done

echo "" >> "$LOG_FILE"
echo "=== Self-Evolution-CN Daily Review Complete (All Agents) ===" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

exit 0
