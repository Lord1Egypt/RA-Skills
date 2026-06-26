#!/bin/bash
# handle-stop.sh - 主Agent处理停止指令的核心脚本
# 版本: 1.0.4
# 功能: 创建stop flag + 读取PID文件 + kill进程 + 清理
# 安全: SESSION_ID格式校验 + PID文件校验 + 进程归属验证 + 审计日志
# 跨平台: Linux + macOS (仅使用POSIX兼容调用)
# 用法: ./handle-stop.sh <SESSION_ID> [reason]
# SESSION_ID格式: {agent-name}-{id} (如 maocaizi-82161)

set -euo pipefail

SESSION_ID="${1:-}"
REASON="${2:-user_request}"
# 防止 JSON 注入：转义 REASON 中的特殊字符
REASON_ESCAPED=$(printf '%s' "$REASON" | sed 's/\\/\\\\/g; s/"/\\"/g; s/`/\\`/g; s/\$/\\$/g')
CURRENT_USER=$(whoami)
AUDIT_LOG="/tmp/agent-interrupt-audit.log"
FLAG_DIR="/tmp"
PID_DIR="/tmp"

# ------------------------------------------------------------------------------
# 审计日志函数
# ------------------------------------------------------------------------------
audit_log() {
    local status="$1"
    local pid="$2"
    local msg="$3"
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "${timestamp} | ${status} | SESSION:${SESSION_ID} | PID:${pid} | USER:${CURRENT_USER} | REASON:${REASON} | ${msg}" >> "${AUDIT_LOG}" 2>/dev/null || true
}

# ------------------------------------------------------------------------------
# SESSION_ID格式校验（豆包建议：严格格式 ^[a-z0-9]+-[a-z0-9]+$）
# ------------------------------------------------------------------------------
validate_session_id() {
    if [ -z "$SESSION_ID" ]; then
        echo "[STOP] 错误: SESSION_ID不能为空"
        echo "[STOP] 用法: $0 <agent-name-id> [reason]"
        echo "[STOP] 示例: $0 maocaizi-82161"
        audit_log "REJECTED" "N/A" "Empty SESSION_ID"
        exit 1
    fi

    # 严格格式校验：仅允许 小写字母+数字 的 {name}-{id} 格式
    if ! [[ "$SESSION_ID" =~ ^[a-z0-9]+-[a-z0-9]+$ ]]; then
        echo "[STOP] 错误: SESSION_ID格式非法"
        echo "[STOP] 必须为 {agent-name}-{id} 格式，如: maocaizi-82161"
        echo "[STOP] 仅允许: 小写字母(a-z) + 数字(0-9) + 短横线(-)"
        audit_log "REJECTED" "N/A" "Invalid SESSION_ID format: ${SESSION_ID}"
        exit 1
    fi

    echo "[STOP] SESSION_ID格式校验通过: ${SESSION_ID}"
}

# ------------------------------------------------------------------------------
# PID文件校验（Kimi建议: 文件类型+所有权+flock原子锁）
# ------------------------------------------------------------------------------
validate_pid_file() {
    local pidfile="$1"

    # 文件必须存在
    if [ ! -f "$pidfile" ]; then
        echo "[STOP] PID文件不存在: $pidfile"
        audit_log "NOT_FOUND" "N/A" "PID file not found"
        return 1
    fi

    # 拒绝符号链接（防止符号链接攻击）
    if [ -L "$pidfile" ]; then
        echo "[STOP] 安全拒绝: PID文件是符号链接: $pidfile"
        audit_log "REJECTED" "N/A" "Symlink PID file rejected"
        return 1
    fi

    # 文件必须普通文件
    if [ ! -f "$pidfile" ]; then
        echo "[STOP] PID文件不是普通文件: $pidfile"
        audit_log "REJECTED" "N/A" "Not a regular file"
        return 1
    fi

    # 文件权限必须是0600或更严格（防止其他用户读取）
    local perms
    perms=$(stat -c '%a' "$pidfile" 2>/dev/null || stat -f '%Lp' "$pidfile" 2>/dev/null || echo "unknown")
    if [ "$perms" != "600" ] && [ "$perms" != "400" ] && [ "$perms" != "700" ] && [ "$perms" != "400" ]; then
        echo "[STOP] 安全警告: PID文件权限过宽($perms): $pidfile"
        audit_log "WARNING" "N/A" "Loose PID file permissions: $perms"
        # 不阻止，但记录警告
    fi

    # 文件必须属于当前用户或root
    local file_owner
    file_owner=$(stat -c '%U' "$pidfile" 2>/dev/null || stat -f '%Su' "$pidfile" 2>/dev/null || echo "unknown")
    if [ "$file_owner" != "$CURRENT_USER" ] && [ "$file_owner" != "root" ]; then
        echo "[STOP] 安全拒绝: PID文件不属于当前用户($CURRENT_USER)或root: owner=$file_owner"
        audit_log "REJECTED" "N/A" "PID file owner mismatch: $file_owner"
        return 1
    fi

    return 0
}

# ------------------------------------------------------------------------------
# 进程验证（命令行标识校验，防止误杀）
# ------------------------------------------------------------------------------
validate_process() {
    local pid="$1"

    # PID必须是纯数字
    if ! [[ "$pid" =~ ^[0-9]+$ ]]; then
        echo "[STOP] 安全拒绝: PID不是有效数字: $pid"
        audit_log "REJECTED" "$pid" "Invalid PID format"
        return 1
    fi

    # 进程必须存在
    if ! ps -p "$pid" > /dev/null 2>&1; then
        echo "[STOP] 进程不存在或已退出: $pid"
        audit_log "ALREADY_DEAD" "$pid" "Process already exited"
        return 1
    fi

    # 读取进程命令行
    local cmdline
    cmdline=$(ps -p "$pid" -o args= 2>/dev/null || echo "")
    if [ -z "$cmdline" ]; then
        echo "[STOP] 无法读取进程命令行: $pid"
        audit_log "REJECTED" "$pid" "Cannot read process cmdline"
        return 1
    fi

    # 验证命令行包含SESSION_ID标识（防误杀无关进程）
    # 注意：这里只记录警告+跳过kill，不拒绝操作
    # 原因：bash -c "var=${var}" 场景命令行不含展开后的值
    # flag机制已能保证优雅退出，kill只是兜底
    if ! echo "$cmdline" | grep -q "${SESSION_ID}"; then
        echo "[STOP] ⚠️ 警告: 进程命令行不包含会话标识 '${SESSION_ID}'"
        echo "[STOP] ⚠️ 可能原因: bash -c变量展开场景或进程已自行退出"
        echo "[STOP] ⚠️ flag机制已创建，依赖优雅退出，跳过kill（兜底保障）"
        echo "[STOP] 📝 进程命令行: $cmdline"
        audit_log "WARN_SKIP_KILL" "$pid" "Cmdline mismatch - skipping kill"
        # 跳过kill，依赖flag机制优雅退出
        rm -f "${PID_FILE}"
        audit_log "CLEANUP_SKIP_KILL" "$pid" "PID file cleaned"
        return 2  # 返回2表示"跳过kill"，不同于返回1"验证失败"
    fi

    echo "[STOP] 进程验证通过: PID=$pid CMD='$cmdline'"
    audit_log "VALIDATED" "$pid" "Process validated"
    return 0
}

# ------------------------------------------------------------------------------
# 主流程
# ------------------------------------------------------------------------------
validate_session_id

FLAG_FILE="${FLAG_DIR}/agent-stop-${SESSION_ID}.flag"
PID_FILE="${PID_DIR}/agent-pid-${SESSION_ID}.pid"

echo "[STOP] ==============================================="
echo "[STOP] Task Interrupt Pro v1.0.2 - 开始中断流程"
echo "[STOP] ==============================================="
echo "[STOP] SESSION_ID: ${SESSION_ID}"
echo "[STOP] 原因: ${REASON}"
echo "[STOP] 当前用户: ${CURRENT_USER}"
echo "[STOP] 审计日志: ${AUDIT_LOG}"

# 步骤1: 创建stop flag（通知进程优雅退出）
echo ""
echo "[STOP] 步骤1: 创建停止标志..."
audit_log "CREATE_FLAG" "N/A" "Creating stop flag"

# 安全检查：拒绝符号链接（防止覆盖任意文件攻击）
if [ -L "${FLAG_FILE}" ]; then
    echo "[STOP] 安全拒绝: FLAG_FILE是符号链接: ${FLAG_FILE}"
    audit_log "REJECTED" "N/A" "Symlink FLAG_FILE rejected"
    exit 1
fi

cat > "${FLAG_FILE}" << EOF
{
  "sessionId": "${SESSION_ID}",
  "timestamp": $(date +%s%3N),
  "reason": "${REASON_ESCAPED}",
  "signal": "SIGINT",
  "createdBy": "${CURRENT_USER}",
  "version": "1.0.2"
}
EOF
chmod 0600 "${FLAG_FILE}"
echo "[STOP] 已创建停止标志: ${FLAG_FILE}"

# 步骤2: 读取PID文件并验证后终止进程
echo ""
echo "[STOP] 步骤2: 读取并验证PID文件..."
if [ -f "${PID_FILE}" ]; then
    if validate_pid_file "${PID_FILE}"; then
        # flock原子锁读取PID（防止竞争条件）
        PID=""
        if command -v flock >/dev/null 2>&1; then
            # 有flock，用原子锁读取
            PID=$(flock -n 100 -c "cat '${PID_FILE}'" 2>/dev/null) || {
                echo "[STOP] flock锁定失败，使用直接读取"
                PID=$(cat "${PID_FILE}")
            }
        else
            # 无flock，直接读取
            PID=$(cat "${PID_FILE}")
        fi

        PID=$(echo "$PID" | tr -cd '[:digit:]')  # 提取纯数字

        if [ -n "$PID" ] && validate_process "$PID"; then
            echo "[STOP] ==============================================="
            echo "[STOP] 准备终止进程: $PID"
            audit_log "TERMINATING" "$PID" "Starting termination"

            # 阶段1: SIGINT（优雅退出，给3秒响应）
            echo "[STOP] 阶段1: 发送SIGINT(优雅)到 $PID..."
            kill -INT "$PID" 2>/dev/null || true

            for i in 1 2 3; do
                sleep 1
                if ! ps -p "$PID" > /dev/null 2>&1; then
                    echo "[STOP] ✅ 进程已通过SIGINT优雅退出"
                    audit_log "SUCCESS" "$PID" "Terminated via SIGINT"
                    break
                fi
                echo "[STOP] 等待进程退出... ($i/3)"
            done

            # 阶段2: SIGTERM
            if ps -p "$PID" > /dev/null 2>&1; then
                echo "[STOP] 阶段2: SIGINT无响应，发送SIGTERM(温和)到 $PID..."
                audit_log "TERM_SENT" "$PID" "SIGINT failed, sending SIGTERM"
                kill -TERM "$PID" 2>/dev/null || true
                sleep 2
            fi

            # 阶段3: SIGKILL
            if ps -p "$PID" > /dev/null 2>&1; then
                echo "[STOP] 阶段3: SIGTERM无响应，执行强制终止(SIGKILL)..."
                audit_log "KILL_SENT" "$PID" "SIGTERM failed, sending SIGKILL"
                kill -9 "$PID" 2>/dev/null || true
                sleep 1
            fi

            # 最终验证
            if ps -p "$PID" > /dev/null 2>&1; then
                echo "[STOP] ⚠️ 警告: 进程 $PID 仍在运行，终止失败"
                audit_log "FAILED" "$PID" "Failed to terminate process"
            else
                echo "[STOP] ✅ 进程已终止: $PID"
            fi
        else
            echo "[STOP] 进程验证失败，跳过终止"
        fi

        # 清理PID文件（无论成功失败都清理）
        rm -f "${PID_FILE}"
        echo "[STOP] 已清理PID文件"
    else
        echo "[STOP] PID文件验证失败，无法终止进程"
    fi
else
    echo "[STOP] 未找到PID文件: ${PID_FILE}"
    echo "[STOP] 提示: 进程可能已自行退出，或SESSION_ID不正确"
    audit_log "NOT_FOUND" "N/A" "PID file not found for termination"
fi

# 步骤3: 60秒后自动清理flag文件
echo ""
echo "[STOP] 步骤3: 安排flag文件60秒后自动清理..."
(
    sleep 60
    if [ -f "${FLAG_FILE}" ]; then
        rm -f "${FLAG_FILE}"
        echo "[STOP] [后台] 60秒后已清理标志文件"
    fi
) &

audit_log "COMPLETED" "N/A" "Interrupt workflow completed"
echo ""
echo "[STOP] ==============================================="
echo "[STOP] 中断流程完成 | SESSION: ${SESSION_ID}"
echo "[STOP] ==============================================="
exit 0
