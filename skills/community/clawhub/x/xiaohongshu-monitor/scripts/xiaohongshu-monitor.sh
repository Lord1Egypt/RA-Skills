#!/bin/bash
# 小红书监测脚本 - 多账号版
# 监控多个博主，支持智能时间调度

# 导出 PATH
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:/usr/bin:/bin:$HOME/.nvm:$HOME/.npm-global/bin:$HOME/bin:$HOME/.volta/bin:$HOME/.asdf/shims:$HOME/.bun/bin:$HOME/Library/Application Support/fnm/aliases/default/bin:$HOME/.fnm/aliases/default/bin:$HOME/Library/pnpm:$HOME/.local/share/pnpm:$PATH"

WORKSPACE="$HOME/.openclaw/workspace"

# 定义要监控的博主列表
# 格式: "ID|名字|快照文件|日志文件"
BLOGGERS=(
    "5b6150c56b58b741e26b8c7f|还是叫吴富贵吧|xiaohongshu-monitor-还是叫吴富贵吧.md|xiaohongshu-monitor-还是叫吴富贵吧.log"
)

# 配置
MAX_RETRIES=3
RETRY_WAIT=10
PAGE_WAIT=8
RATE_LIMIT_WAIT=60
OPENCLAW="/opt/homebrew/bin/openclaw"

log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $1"
    echo "$msg" | tee -a "$LOG_FILE" >&2
}

# 清理标题
clean_title() {
    local blogger_name="$1"
    echo "$2" | sed -E 's/^置顶[[:space:]]*//' \
                     | sed -E "s/$blogger_name//g" \
                     | sed -E 's/^momo[[:space:]]*//' \
                     | sed -E 's/[0-9.]*万//g' \
                     | sed -E 's/[0-9]+//g' \
                     | sed -E 's/^[[:space:]]*//;s/[[:space:]]*$//' \
                     | sed -E 's/[[:space:]]+/ /g'
}

is_valid_result() {
    local result="$1"
    if [ -z "$result" ]; then
        return 1
    fi
    if echo "$result" | grep -qE "UtilityScript|Bind:|error|Error|undefined|at <anonymous>|请求太频繁"; then
        return 1
    fi
    return 0
}

# 打开浏览器
open_browser() {
    local target_url="$1"
    local retry=0
    while [ $retry -lt $MAX_RETRIES ]; do
        BROWSER_RESULT=$("$OPENCLAW" browser --profile openclaw open "$target_url" 2>&1)
        TARGET_ID=$(echo "$BROWSER_RESULT" | grep -oE 'id:[[:space:]]*[a-zA-Z0-9]+' | awk '{print $2}')
        if [ -z "$TARGET_ID" ]; then
            TARGET_ID=$(echo "$BROWSER_RESULT" | grep -oE 'opened:.*$' | sed 's/opened:.*id: //' | tail -1)
        fi
        if [ -n "$TARGET_ID" ]; then
            return 0
        fi
        retry=$((retry+1))
        [ $retry -lt $MAX_RETRIES ] && sleep $RETRY_WAIT
    done
    return 1
}

# 获取帖子列表
fetch_posts() {
    local retry=0
    while [ $retry -lt $MAX_RETRIES ]; do
        sleep $PAGE_WAIT
        RESULT=$("$OPENCLAW" browser evaluate \
            --target-id "$TARGET_ID" \
            --fn "Array.from(document.querySelectorAll('[class*=\"note-item\"], [class*=\"user-post\"], section[class*=\"note\"]')).slice(0,15).map(el => { const title = el.textContent.trim().split('\\n')[0].trim(); return title.length > 0 ? title : null; }).filter(t => t !== null).slice(0,10).join('|||')" \
            2>&1 | tail -1)
        RESULT=$(echo "$RESULT" | sed 's/^"\(.*\)"$/\1/' | sed 's/\\"/"/g')
        
        if echo "$RESULT" | grep -q "请求太频繁"; then
            sleep $RATE_LIMIT_WAIT
            retry=$((retry+1))
            continue
        fi
        
        if is_valid_result "$RESULT"; then
            return 0
        fi
        retry=$((retry+1))
        [ $retry -lt $MAX_RETRIES ] && sleep $RETRY_WAIT
    done
    return 1
}

# 关闭浏览器
close_browser() {
    [ -n "$TARGET_ID" ] && "$OPENCLAW" browser close "$TARGET_ID" 2>/dev/null
}

# 加载旧快照
load_snapshot() {
    local blogger_name="$1"
    local snapshot_file="$2"
    if [ ! -f "$WORKSPACE/memory/$snapshot_file" ]; then
        echo ""
        return
    fi
    sed '1,4d' "$WORKSPACE/memory/$snapshot_file" 2>/dev/null | grep -E "^[0-9]+\." | sed 's/^[0-9]*\. //' | while read -r line; do
        clean_title "$blogger_name" "$line"
    done
}

# 找新帖子
find_new_posts() {
    local blogger_name="$1"
    local current="$2"
    local old_snapshot="$3"
    
    local -a current_arr=()
    local IFS='|||'
    for item in $current; do
        item=$(echo "$item" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
        [ -z "$item" ] && continue
        local cleaned=$(clean_title "$blogger_name" "$item")
        if [ -n "$cleaned" ] && [ ${#cleaned} -ge 2 ]; then
            current_arr+=("$cleaned")
        fi
    done
    
    local -a old_arr=()
    while IFS= read -r line; do
        [ -n "$line" ] && old_arr+=("$line")
    done <<< "$old_snapshot"
    
    local new_posts=""
    for curr in "${current_arr[@]}"; do
        local found=0
        for old in "${old_arr[@]}"; do
            if [ "$curr" = "$old" ]; then
                found=1
                break
            fi
        done
        [ $found -eq 0 ] && new_posts+="$curr"$'\n'
    done
    
    [ -n "$new_posts" ] && echo "$new_posts" | sed '/^$/d'
}

# 保存快照
save_snapshot() {
    local blogger_name="$1"
    local snapshot_file="$2"
    local current="$3"
    
    {
        echo "# 小红书博主监测快照"
        echo "# 博主: $blogger_name"
        echo "# 更新时间: $(date)"
        echo ""
        
        local IFS='|||'
        local i=1
        for item in $current; do
            item=$(echo "$item" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
            [ -z "$item" ] && continue
            local cleaned=$(clean_title "$blogger_name" "$item")
            [ -n "$cleaned" ] && [ ${#cleaned} -ge 2 ] && echo "$i. $cleaned" && i=$((i+1))
        done
    } > "$WORKSPACE/memory/$snapshot_file"
}

# 发送通知
send_notification() {
    local blogger_name="$1"
    local new_posts="$2"
    
    [ -z "$new_posts" ] && return
    
    local msg="🔔 小红书博主「$blogger_name」发新帖子啦：\n\n"
    
    local i=1
    while IFS= read -r line; do
        [ -n "$line" ] && msg+="$i. $line\n" && i=$((i+1))
    done <<< "$new_posts"
    
    "$OPENCLAW" message send \
        --target "ou_24c2bc2b000e0ea7a99dea7f4f657dbc" \
        --message "$msg" \
        2>&1 | tail -1
}

# 监控单个博主
monitor_one() {
    local blogger_info="$1"
    local user_id=$(echo "$blogger_info" | cut -d'|' -f1)
    local blogger_name=$(echo "$blogger_info" | cut -d'|' -f2)
    local snapshot_file=$(echo "$blogger_info" | cut -d'|' -f3)
    local log_file=$(echo "$blogger_info" | cut -d'|' -f4)
    
    LOG_FILE="$WORKSPACE/memory/$log_file"
    local target_url="https://www.xiaohongshu.com/user/profile/$user_id"
    
    log "========== 开始检查博主: $blogger_name =========="
    
    if ! open_browser "$target_url"; then
        log "浏览器打开失败"
        return 1
    fi
    
    if ! fetch_posts; then
        close_browser
        log "获取帖子失败"
        return 1
    fi
    
    close_browser
    
    local old_snapshot=$(load_snapshot "$blogger_name" "$snapshot_file")
    local new_posts=$(find_new_posts "$blogger_name" "$RESULT" "$old_snapshot")
    
    if [ -n "$new_posts" ]; then
        log "发现新帖子: $new_posts"
        send_notification "$blogger_name" "$new_posts"
        save_snapshot "$blogger_name" "$snapshot_file" "$RESULT"
    else
        log "没有新帖子"
    fi
    
    log "========== 检查完成 =========="
}

# 主函数 - 直接遍历所有博主检查
main() {
    for blogger in "${BLOGGERS[@]}"; do
        monitor_one "$blogger"
    done
}

main
