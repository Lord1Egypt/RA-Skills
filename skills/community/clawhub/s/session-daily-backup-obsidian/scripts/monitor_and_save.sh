#!/bin/bash
# Token-free conversation monitoring and auto-save
# 每日增量备份 - 无 LLM 调用，仅在需要警告时发送 QQ 通知

# 加载配置
CONFIG_FILE="$(dirname "$0")/../config"
if [[ -f "$CONFIG_FILE" ]]; then
    source "$CONFIG_FILE"
fi

# 默认路径（如果配置未设置）
SESSION_DIR="${SESSION_DIR:-/root/.openclaw/agents/main/sessions}"
VAULT_DIR="${VAULT_DIR:-$HOME/Documents/Obsidian/Clawd Markdowns}"
LAST_SNAPSHOT_FILE="${TRACKING_DIR:-/root/clawd}/.last_snapshot_timestamp"
WARNING_SENT_FILE="${TRACKING_DIR:-/root/clawd}/.token_warning_sent"
FORMAT_JQ="${TRACKING_DIR:-/root/clawd}/format_message_v2.jq"

# 获取最新的 session 文件
get_latest_session() {
    ls -t "$SESSION_DIR"/*.jsonl 2>/dev/null | head -1
}

# 估算 token 数（粗略：1 token ≈ 4 字符）
estimate_tokens() {
    local file="$1"
    if [[ ! -f "$file" ]]; then
        echo 0
        return
    fi
    local chars=$(wc -c < "$file")
    echo $((chars / 4))
}

# 获取当前行数
get_line_count() {
    local file="$1"
    if [[ ! -f "$file" ]]; then
        echo 0
        return
    fi
    wc -l < "$file"
}

# 将 JSONL 转换为 markdown 对话（Obsidian 聊天格式）
jsonl_to_markdown() {
    local jsonl_file="$1"
    local start_line="${2:-1}"
    
    tail -n +$start_line "$jsonl_file" | while IFS= read -r line; do
        echo "$line" | jq -r -f "$FORMAT_JQ" 2>/dev/null
    done
}

# 发送 QQ 警告消息
send_qq_warning() {
    local message="$1"
    
    # 方法 1: 使用 openclaw message 工具（如果可用）
    if command -v openclaw &> /dev/null; then
        openclaw message send --channel qqbot --message "$message" 2>/dev/null
        return $?
    fi
    
    # 方法 2: 使用 go-cqhttp API（如果配置了）
    if [[ -n "$QQ_BOT_URL" ]]; then
        curl -s -X POST "$QQ_BOT_URL/send_private_msg" \
            -H "Content-Type: application/json" \
            -d "{\"user_id\": \"$QQ_USER_ID\", \"message\": \"$message\"}" > /dev/null
        return $?
    fi
    
    # 方法 3: 记录到日志（如果其他方式都不可用）
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] QQ WARNING: $message" >> "${TRACKING_DIR:-/root/clawd}/qq_warnings.log"
    return 0
}

# 保存对话快照（备份当天所有 session）
save_snapshot() {
    local timestamp=$(date +"%Y-%m-%d")
    local snapshot_file="$VAULT_DIR/$timestamp-daily.md"
    
    # 获取所有 session 文件
    local session_files=($(ls -t "$SESSION_DIR"/*.jsonl 2>/dev/null))
    
    if [[ ${#session_files[@]} -eq 0 ]]; then
        echo "ℹ️  未找到 session 文件"
        return
    fi
    
    # 计算总 token 数和行数
    local total_tokens=0
    local total_lines=0
    local session_count=${#session_files[@]}
    
    for session_file in "${session_files[@]}"; do
        total_tokens=$((total_tokens + $(estimate_tokens "$session_file")))
        total_lines=$((total_lines + $(wc -l < "$session_file")))
    done
    
    # 获取上次备份的总行数
    local last_saved_total=$(cat "$LAST_SNAPSHOT_FILE" 2>/dev/null || echo 0)
    local new_lines=$((total_lines - last_saved_total))
    
    # 只有当有至少 10 条新消息时才保存
    if [[ $new_lines -lt 10 ]]; then
        echo "ℹ️  无足够新消息（$new_lines < 10），跳过备份"
        return
    fi
    
    # 创建或追加文件
    if [[ ! -f "$snapshot_file" ]]; then
        cat > "$snapshot_file" <<EOF
# 每日对话备份 - $timestamp

**自动保存时间**: $(date '+%Y-%m-%d %H:%M %Z')
**Token 估算**: ${total_tokens}k/1,000,000 ($(( (total_tokens * 100) / 1000000 ))%)
**Session 数量**: $session_count
**总消息数**: $total_lines 行
**本次新增**: $new_lines 行

---

EOF
    else
        echo "" >> "$snapshot_file"
        echo "---" >> "$snapshot_file"
        echo "" >> "$snapshot_file"
        echo "## 新增对话 - $(date '+%H:%M')" >> "$snapshot_file"
        echo "" >> "$snapshot_file"
    fi
    
    # 备份所有 session 文件
    local saved_count=0
    for session_file in "${session_files[@]}"; do
        local session_name=$(basename "$session_file" .jsonl)
        local session_lines=$(wc -l < "$session_file")
        
        echo "" >> "$snapshot_file"
        echo "### 📁 Session: $session_name ($session_lines 行)" >> "$snapshot_file"
        echo "" >> "$snapshot_file"
        
        # 转换整个 session 为 markdown
        cat "$session_file" | while IFS= read -r line; do
            echo "$line" | jq -r -f "$FORMAT_JQ" 2>/dev/null
        done >> "$snapshot_file"
        
        saved_count=$((saved_count + session_lines))
    done
    
    # 更新跟踪文件
    echo "$total_lines" > "$LAST_SNAPSHOT_FILE"
    
    echo "✅ 已保存每日备份：$snapshot_file（$session_count 个 session，共 $saved_count 行）"
}

# 主逻辑
SESSION_FILE=$(get_latest_session)

if [[ ! -f "$SESSION_FILE" ]]; then
    echo "ℹ️  未找到 session 文件"
    exit 0
fi

TOKENS=$(estimate_tokens "$SESSION_FILE")
CURRENT_LINES=$(get_line_count "$SESSION_FILE")

echo "📊 当前状态:"
echo "   Token 数：${TOKENS}k"
echo "   总行数：$CURRENT_LINES"

# 自动保存增量快照
save_snapshot

# Token 警告（仅在跨越阈值时发送）
if [[ $TOKENS -gt 900000 ]]; then
    if [[ ! -f "$WARNING_SENT_FILE" ]] || [[ $(cat "$WARNING_SENT_FILE") != "900k" ]]; then
        echo "🚨 发送紧急警告（90%+）..."
        send_qq_warning "🚨 紧急：上下文已达 ${TOKENS}k/1M (90%+) - 请立即运行 /new"
        echo "900k" > "$WARNING_SENT_FILE"
    fi
elif [[ $TOKENS -gt 800000 ]]; then
    if [[ ! -f "$WARNING_SENT_FILE" ]] || [[ $(cat "$WARNING_SENT_FILE") != "800k" ]]; then
        echo "⚠️  发送警告（80%+）..."
        send_qq_warning "⚠️  Token 警告：上下文已达 ${TOKENS}k/1M (80%+) - 建议尽快运行 /new"
        echo "800k" > "$WARNING_SENT_FILE"
    fi
else
    # 当低于阈值时重置警告标志
    rm -f "$WARNING_SENT_FILE" 2>/dev/null
fi

exit 0
