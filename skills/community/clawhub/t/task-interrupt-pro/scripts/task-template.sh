#!/bin/bash
# task-template.sh - Subagent可中断任务模板
# 版本: 1.0.2
# 功能: PID记录 + flag检查 + trap信号处理 + 审计日志
# SESSION_ID格式: {agent-name}-{id} (如 maocaizi-82161)
# 用法: 替换模板中的 YOUR_TASK_HERE 为实际任务逻辑

set -euo pipefail

# SESSION_ID必须传入
if [ -z "${1:-}" ]; then
    echo "[TEMPLATE] 错误: 请传入SESSION_ID参数"
    echo "[TEMPLATE] 用法: bash task-template.sh <agent-name-id>"
    echo "[TEMPLATE] 示例: bash task-template.sh maocaizi-82161"
    exit 1
fi

SESSION_ID="$1"
AUDIT_LOG="/tmp/agent-interrupt-audit.log"
FLAG_DIR="/tmp"
PID_DIR="/tmp"
FLAG_FILE="${FLAG_DIR}/agent-stop-${SESSION_ID}.flag"
PID_FILE="${PID_DIR}/agent-pid-${SESSION_ID}.pid"

# ------------------------------------------------------------------------------
# SESSION_ID格式校验（严格格式）
# ------------------------------------------------------------------------------
if ! [[ "$SESSION_ID" =~ ^[a-z0-9]+-[a-z0-9]+$ ]]; then
    echo "[TEMPLATE] 错误: SESSION_ID格式非法: ${SESSION_ID}"
    echo "[TEMPLATE] 必须为 {agent-name}-{id} 格式，如: maocaizi-82161"
    exit 1
fi

# ------------------------------------------------------------------------------
# 审计日志
# ------------------------------------------------------------------------------
audit_log() {
    local status="$1"
    local msg="$2"
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "${timestamp} | ${status} | SESSION:${SESSION_ID} | PID:$$ | ${msg}" >> "${AUDIT_LOG}" 2>/dev/null || true
}

# ------------------------------------------------------------------------------
# 目录创建
# ------------------------------------------------------------------------------
mkdir -p "${PID_DIR}" 2>/dev/null || true
chmod 0755 "${PID_DIR}" 2>/dev/null || true

# ------------------------------------------------------------------------------
# PID文件写入（使用flock原子锁，防止竞争条件）
# ------------------------------------------------------------------------------
write_pid() {
    if command -v flock >/dev/null 2>&1; then
        # 有flock，用原子锁写入
        flock -n 200 -c "echo $$ > '${PID_FILE}' && chmod 0600 '${PID_FILE}'" 200>"${PID_FILE}.lock" 2>/dev/null || {
            echo "[TEMPLATE] flock锁定失败，使用直接写入"
            echo $$ > "${PID_FILE}"
            chmod 0600 "${PID_FILE}"
        }
    else
        # 无flock，直接写入
        echo $$ > "${PID_FILE}"
        chmod 0600 "${PID_FILE}"
    fi
}

# ------------------------------------------------------------------------------
# 清理函数
# ------------------------------------------------------------------------------
cleanup() {
    local exit_code=$?
    echo "[TRAP] 收到停止信号，开始清理..."
    audit_log "CLEANUP" "Exit code: $exit_code"

    # 清理PID文件
    rm -f "${PID_FILE}" 2>/dev/null || true
    rm -f "${PID_FILE}.lock" 2>/dev/null || true

    echo "[TRAP] 清理完成，PID文件已删除"
    exit $exit_code
}

# ------------------------------------------------------------------------------
# 信号处理（收到SIGINT/SIGTERM时优雅退出）
# ------------------------------------------------------------------------------
trap 'echo "[TRAP] 收到SIGINT/SIGTERM信号"; cleanup' SIGINT SIGTERM

# ------------------------------------------------------------------------------
# 退出时清理（无论正常还是异常退出）
# ------------------------------------------------------------------------------
trap 'audit_log "EXIT" "Process exited"' EXIT

# ------------------------------------------------------------------------------
# 主流程
# ------------------------------------------------------------------------------
echo "[TEMPLATE] ==============================================="
echo "[TEMPLATE] 可中断任务模板 v1.0.2"
echo "[TEMPLATE] SESSION_ID: ${SESSION_ID}"
echo "[TEMPLATE] PID: $$"
echo "[TEMPLATE] PID_FILE: ${PID_FILE}"
echo "[TEMPLATE] FLAG_FILE: ${FLAG_FILE}"
echo "[TEMPLATE] ==============================================="

# 写入PID文件
write_pid
audit_log "STARTED" "Task started with PID $$"

# 主循环
counter=0
while true; do
    counter=$((counter + 1))

    # 检查stop flag（发现后优雅退出）
    if [ -f "${FLAG_FILE}" ]; then
        echo "[TEMPLATE] 检测到停止标志，优雅退出"
        audit_log "FLAG_STOP" "Stop flag detected, exiting gracefully"
        cleanup
    fi

    # ========== 替换为你实际的任务逻辑 ==========
    echo "[TEMPLATE] [${counter}] 工作中... $(date '+%H:%M:%S') PID:$$ SESSION:${SESSION_ID}"
    # 示例：sleep 2
    sleep 3
    # ==========================================

done
