#!/bin/bash
# 任务保障工具函数库
# 用法：source /home/admin/.openclaw/workspace/scripts/task-utils.sh

WORKSPACE="/home/admin/.openclaw/workspace"
TASK_REGISTRY="$WORKSPACE/memory/task-registry.json"
TASKS_DIR="$WORKSPACE/memory/tasks"
LOGS_DIR="$WORKSPACE/logs/tasks"

# 确保目录存在
mkdir -p "$TASKS_DIR" "$LOGS_DIR"

# 初始化任务
# 用法：task_init "task_id" "任务名称" ["描述"]
task_init() {
    local task_id=$1
    local task_name=$2
    local description=${3:-$task_name}
    local timestamp=$(date -Iseconds)
    
    # 创建状态文件
    cat > "$TASKS_DIR/${task_id}.json" << EOF
{
  "taskId": "$task_id",
  "name": "$task_name",
  "description": "$description",
  "status": "pending",
  "stages": [],
  "logs": [],
  "errors": [],
  "createdAt": "$timestamp",
  "startedAt": null,
  "completedAt": null,
  "duration": null
}
EOF
    
    # 记录日志
    task_log "$task_id" "INFO" "任务初始化：$task_name"
    
    echo "✅ 任务已初始化：$task_id"
}

# 更新任务状态
# 用法：task_update "task_id" "status" ["message"]
task_update() {
    local task_id=$1
    local status=$2
    local message=${3:-}
    local timestamp=$(date -Iseconds)
    
    local state_file="$TASKS_DIR/${task_id}.json"
    
    if [ ! -f "$state_file" ]; then
        echo "❌ 任务不存在：$task_id"
        return 1
    fi
    
    # 更新状态
    local updated=$(jq --arg s "$status" --arg t "$timestamp" \
        '.status = $s | .startedAt = (.startedAt // $t)' "$state_file")
    
    echo "$updated" > "$state_file"
    
    if [ -n "$message" ]; then
        task_log "$task_id" "INFO" "$message"
    fi
}

# 开始任务
# 用法：task_start "task_id"
task_start() {
    local task_id=$1
    local timestamp=$(date -Iseconds)
    
    task_update "$task_id" "running" "任务开始执行"
    
    # 添加阶段
    local state_file="$TASKS_DIR/${task_id}.json"
    local updated=$(jq --arg t "$timestamp" \
        '.stages += [{"name": "执行", "status": "running", "timestamp": $t}]' "$state_file")
    echo "$updated" > "$state_file"
}

# 记录日志
# 用法：task_log "task_id" "LEVEL" "message"
task_log() {
    local task_id=$1
    local level=$2
    local message=$3
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local log_entry="[$timestamp] [$level] $message"
    
    # 追加到日志文件
    echo "$log_entry" >> "$LOGS_DIR/${task_id}.log"
    
    # 同时追加到状态文件的 logs 数组
    local state_file="$TASKS_DIR/${task_id}.json"
    if [ -f "$state_file" ]; then
        local updated=$(jq --arg log "$log_entry" '.logs += [$log]' "$state_file")
        echo "$updated" > "$state_file"
    fi
}

# 添加阶段
# 用法：task_stage "task_id" "阶段名" "status"
task_stage() {
    local task_id=$1
    local stage_name=$2
    local status=$3
    local timestamp=$(date -Iseconds)
    
    local state_file="$TASKS_DIR/${task_id}.json"
    local updated=$(jq --arg n "$stage_name" --arg s "$status" --arg t "$timestamp" \
        '.stages += [{"name": $n, "status": $s, "timestamp": $t}]' "$state_file")
    echo "$updated" > "$state_file"
}

# 完成任务
# 用法：task_complete "task_id" ["result_message"]
task_complete() {
    local task_id=$1
    local result=${2:-"任务完成"}
    local timestamp=$(date -Iseconds)
    local state_file="$TASKS_DIR/${task_id}.json"
    
    # 计算耗时
    local started_at=$(jq -r '.startedAt // .createdAt' "$state_file")
    local start_epoch=$(date -d "$started_at" +%s 2>/dev/null || date -Iseconds)
    local end_epoch=$(date -d "$timestamp" +%s 2>/dev/null || date -Iseconds)
    local duration=$((end_epoch - start_epoch))
    
    # 更新状态
    local updated=$(jq --arg s "success" --arg t "$timestamp" --arg d "$duration" --arg r "$result" \
        '.status = $s | .completedAt = $t | .duration = ($d | tonumber) | .result = $r | .stages[-1].status = "done"' "$state_file")
    echo "$updated" > "$state_file"
    
    task_log "$task_id" "INFO" "✅ 任务完成：$result (耗时：${duration}s)"
    
    echo "✅ 任务完成：$task_id"
}

# 任务失败
# 用法：task_fail "task_id" "error_message" ["error_type"]
task_fail() {
    local task_id=$1
    local error=$2
    local error_type=${3:-"unknown_error"}
    local timestamp=$(date -Iseconds)
    local state_file="$TASKS_DIR/${task_id}.json"
    
    # 分析错误类型
    local analysis=""
    case "$error_type" in
        "command_not_found")
            analysis="命令未找到，检查 PATH 或安装依赖"
            ;;
        "authentication_failed")
            analysis="认证失败，检查配置或凭证"
            ;;
        "network_error")
            analysis="网络错误，检查连接或重试"
            ;;
        "timeout")
            analysis="执行超时，增加超时时间或优化"
            ;;
        "resource_not_found")
            analysis="资源不存在，检查路径或创建"
            ;;
        "permission_denied")
            analysis="权限不足，检查权限设置"
            ;;
        *)
            analysis="需人工排查"
            ;;
    esac
    
    # 更新状态
    local updated=$(jq --arg s "failed" --arg t "$timestamp" --arg e "$error" --arg et "$error_type" --arg a "$analysis" \
        '.status = $s | .errors += [{"time": $t, "message": $e, "type": $et, "analysis": $a}] | .stages[-1].status = "failed"' "$state_file")
    echo "$updated" > "$state_file"
    
    task_log "$task_id" "ERROR" "❌ 任务失败：$error (类型：$error_type)"
    task_log "$task_id" "INFO" "🔍 分析：$analysis"
    
    echo "⚠️ 任务失败：$task_id"
    echo "   错误：$error"
    echo "   类型：$error_type"
    echo "   分析：$analysis"
    echo "   请检查：$state_file"
}

# 获取任务状态
# 用法：task_status "task_id"
task_status() {
    local task_id=$1
    local state_file="$TASKS_DIR/${task_id}.json"
    
    if [ ! -f "$state_file" ]; then
        echo "❌ 任务不存在：$task_id"
        return 1
    fi
    
    jq '.' "$state_file"
}

# 重试任务（带退避）
# 用法：task_retry "task_id" "max_retries" ["retry_interval_seconds"]
task_retry() {
    local task_id=$1
    local max_retries=${2:-3}
    local interval=${3:-60}
    
    local state_file="$TASKS_DIR/${task_id}.json"
    local current_status=$(jq -r '.status' "$state_file")
    
    if [ "$current_status" != "failed" ]; then
        echo "⚠️ 任务当前状态不是 failed，无需重试"
        return 1
    fi
    
    local retry_count=$(jq '.errors | length' "$state_file")
    
    if [ "$retry_count" -gt "$max_retries" ]; then
        echo "❌ 已达到最大重试次数 ($max_retries)"
        return 1
    fi
    
    echo "🔄 重试任务：$task_id (第 $retry_count 次，共 $max_retries 次)"
    echo "⏱️ 等待 ${interval} 秒..."
    sleep "$interval"
    
    # 重置状态为 pending
    task_update "$task_id" "pending" "准备重试（第 $retry_count 次）"
}

# 列出所有任务
# 用法：task_list
task_list() {
    echo "📋 任务列表："
    echo "============"
    
    for state_file in "$TASKS_DIR"/*.json; do
        if [ -f "$state_file" ]; then
            local task_id=$(jq -r '.taskId' "$state_file")
            local task_name=$(jq -r '.name' "$state_file")
            local status=$(jq -r '.status' "$state_file")
            local completed=$(jq -r '.completedAt // "未完成"' "$state_file")
            
            printf "%-30s %-20s %-10s %s\n" "$task_id" "$task_name" "$status" "$completed"
        fi
    done
}

# 清理过期任务（可选）
# 用法：task_cleanup "days"
task_cleanup() {
    local days=${1:-30}
    local cutoff=$(date -d "$days days ago" -Iseconds 2>/dev/null || date -Iseconds)
    
    echo "🧹 清理 $days 天前的任务..."
    
    for state_file in "$TASKS_DIR"/*.json; do
        if [ -f "$state_file" ]; then
            local completed=$(jq -r '.completedAt // empty' "$state_file")
            if [ -n "$completed" ]; then
                # 比较时间（简化处理）
                local log_file="$LOGS_DIR/$(basename "$state_file" .json).log"
                echo "📁 归档：$(basename "$state_file")"
                # 实际清理逻辑可根据需要添加
            fi
        fi
    done
}

# 导出函数
export -f task_init task_update task_start task_log task_stage
export -f task_complete task_fail task_status task_retry task_list task_cleanup
