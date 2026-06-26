#!/bin/bash
# 会话清理脚本

set -e

WORKSPACE="$HOME/.openclaw/workspace"
CONFIG_DIR="$HOME/.openclaw/session-manager"
SESSIONS_DIR="$HOME/.openclaw/agents/main/sessions"
LOG_FILE="$CONFIG_DIR/cleanup.log"

# 默认配置
MAX_AGE_DAYS=7
MIN_SESSIONS=5
WHITELIST=("main" "heartbeat")

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --max-age)
            MAX_AGE_DAYS="$2"
            shift 2
            ;;
        --min-sessions)
            MIN_SESSIONS="$2"
            shift 2
            ;;
        --whitelist)
            IFS=',' read -ra WHITELIST <<< "$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        *)
            echo "未知参数: $1"
            exit 1
            ;;
    esac
done

# 读取配置文件（如果存在）
if [ -f "$CONFIG_DIR/config.json" ]; then
    if command -v jq &> /dev/null; then
        CONFIG_MAX_AGE=$(jq -r '.maxAgeDays // empty' "$CONFIG_DIR/config.json" 2>/dev/null || echo "")
        CONFIG_MIN_SESSIONS=$(jq -r '.minSessions // empty' "$CONFIG_DIR/config.json" 2>/dev/null || echo "")
        CONFIG_WHITELIST=$(jq -r '.whitelist[] // empty' "$CONFIG_DIR/config.json" 2>/dev/null || echo "")
        
        [ -n "$CONFIG_MAX_AGE" ] && MAX_AGE_DAYS=$CONFIG_MAX_AGE
        [ -n "$CONFIG_MIN_SESSIONS" ] && MIN_SESSIONS=$CONFIG_MIN_SESSIONS
        if [ -n "$CONFIG_WHITELIST" ]; then
            WHITELIST=()
            while IFS= read -r item; do
                WHITELIST+=("$item")
            done < <(jq -r '.whitelist[]' "$CONFIG_DIR/config.json" 2>/dev/null)
        fi
    fi
fi

echo "🧹 会话清理"
echo "============"
echo "保留天数: $MAX_AGE_DAYS 天"
echo "最少保留: $MIN_SESSIONS 个会话"
echo "白名单: ${WHITELIST[*]}"
echo ""

# 检查会话目录
if [ ! -d "$SESSIONS_DIR" ]; then
    echo "⚠️  会话目录不存在: $SESSIONS_DIR"
    exit 0
fi

# 获取所有会话文件
SESSION_FILES=("$SESSIONS_DIR"/*.json)
SESSION_COUNT=${#SESSION_FILES[@]}

if [ "$SESSION_COUNT" -eq 1 ] && [ ! -f "${SESSION_FILES[0]}" ]; then
    echo "✅ 无会话文件，无需清理"
    exit 0
fi

echo "发现 $SESSION_COUNT 个会话文件"

# 计算删除截止时间
CUTOFF_TIME=$(( $(date +%s) - (MAX_AGE_DAYS * 86400) ))

# 收集可删除的会话
TO_DELETE=()
TO_KEEP=()

for session_file in "${SESSION_FILES[@]}"; do
    if [ ! -f "$session_file" ]; then
        continue
    fi
    
    # 获取会话 ID（文件名）
    session_id=$(basename "$session_file" .json)
    
    # 检查是否在白名单中
    is_whitelisted=false
    for whitelist_item in "${WHITELIST[@]}"; do
        if [[ "$session_id" == "$whitelist_item"* ]]; then
            is_whitelisted=true
            break
        fi
    done
    
    if [ "$is_whitelisted" = true ]; then
        TO_KEEP+=("$session_file")
        continue
    fi
    
    # 获取文件修改时间
    file_mtime=$(stat -c %Y "$session_file" 2>/dev/null || stat -f %m "$session_file" 2>/dev/null || echo "0")
    
    if [ "$file_mtime" -lt "$CUTOFF_TIME" ]; then
        TO_DELETE+=("$session_file")
    else
        TO_KEEP+=("$session_file")
    fi
done

DELETE_COUNT=${#TO_DELETE[@]}
KEEP_COUNT=${#TO_KEEP[@]}

echo "计划保留: $KEEP_COUNT 个会话"
echo "计划删除: $DELETE_COUNT 个会话"

# 确保最少保留指定数量的会话
if [ "$KEEP_COUNT" -lt "$MIN_SESSIONS" ]; then
    echo "⚠️  保留会话数 ($KEEP_COUNT) 少于最小值 ($MIN_SESSIONS)，调整删除策略"
    
    # 按时间排序，保留最新的
    ALL_SESSIONS=("${SESSION_FILES[@]}")
    IFS=$'\n' sorted_sessions=($(sort -k2 -n <<<"${ALL_SESSIONS[*]/%$'\t'%$(stat -c %Y {} 2>/dev/null || stat -f %m {} 2>/dev/null || echo "0")}"))
    
    # 重新计算要保留的会话
    TO_KEEP=()
    TO_DELETE=()
    
    for i in "${!sorted_sessions[@]}"; do
        session_file="${sorted_sessions[$i]}"
        if [ ! -f "$session_file" ]; then
            continue
        fi
        
        session_id=$(basename "$session_file" .json)
        
        # 白名单优先
        is_whitelisted=false
        for whitelist_item in "${WHITELIST[@]}"; do
            if [[ "$session_id" == "$whitelist_item"* ]]; then
                is_whitelisted=true
                break
            fi
        done
        
        if [ "$is_whitelisted" = true ]; then
            TO_KEEP+=("$session_file")
        elif [ "${#TO_KEEP[@]}" -lt "$MIN_SESSIONS" ]; then
            TO_KEEP+=("$session_file")
        else
            TO_DELETE+=("$session_file")
        fi
    done
    
    DELETE_COUNT=${#TO_DELETE[@]}
    KEEP_COUNT=${#TO_KEEP[@]}
    echo "调整后 - 保留: $KEEP_COUNT, 删除: $DELETE_COUNT"
fi

# 执行删除
if [ "$DELETE_COUNT" -gt 0 ]; then
    echo ""
    if [ "$DRY_RUN" = true ]; then
        echo "🧪 干运行模式（不会实际删除）:"
        for file in "${TO_DELETE[@]}"; do
            echo "  - $(basename "$file")"
        done
    else
        echo "🗑️  删除 $DELETE_COUNT 个会话:"
        for file in "${TO_DELETE[@]}"; do
            rm -f "$file"
            echo "  - $(basename "$file")"
            
            # 记录日志
            echo "$(date '+%Y-%m-%d %H:%M:%S') - 删除会话: $(basename "$file")" >> "$LOG_FILE"
        done
        echo "✅ 清理完成！"
    fi
else
    echo "✅ 无需清理"
fi

# 输出统计信息
echo ""
echo "📊 清理统计:"
echo "  总会话数: $SESSION_COUNT"
echo "  保留会话: $KEEP_COUNT"
echo "  删除会话: $DELETE_COUNT"
echo "  日志文件: $LOG_FILE"