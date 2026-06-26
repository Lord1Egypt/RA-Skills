#!/bin/bash
# 飞书日历和会议室操作脚本 - 自动化版本

set -e

# 配置
APP_ID="cli_a92fba8c65e35cc4"
APP_SECRET="UFUvM2wNSkErIxe7t63ZrgyecakLwNQR"
DEFAULT_USER_OPEN_ID="ou_59348e484376ec5bcf387cb22888dfac"  # 默认用户

CREDENTIALS_DIR="/root/.openclaw/credentials"
AUTHORIZED_USERS_FILE="$CREDENTIALS_DIR/feishu-authorized-users.json"
TOKEN_FILE="$CREDENTIALS_DIR/feishu-user-token.json"

# 获取 tenant_access_token
get_tenant_token() {
    curl -s "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
        -H "Content-Type: application/json" \
        -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" | jq -r '.tenant_access_token'
}

# 获取有效的 user_access_token（自动刷新）
get_valid_user_token() {
    local user_open_id="${1:-$DEFAULT_USER_OPEN_ID}"
    
    # 从多用户文件获取
    if [ -f "$AUTHORIZED_USERS_FILE" ]; then
        local token_data=$(cat "$AUTHORIZED_USERS_FILE" | jq -r --arg id "$user_open_id" '.[$id] // empty')
        
        if [ -n "$token_data" ] && [ "$token_data" != "null" ]; then
            local access_token=$(echo "$token_data" | jq -r '.access_token // empty')
            local expires_at=$(echo "$token_data" | jq -r '.expires_at // 0')
            local refresh_token=$(echo "$token_data" | jq -r '.refresh_token // empty')
            local now=$(date +%s)
            
            # Token 有效（预留5分钟缓冲）
            if [ -n "$access_token" ] && [ "$expires_at" -gt "$((now + 300))" ]; then
                echo "$access_token"
                return 0
            fi
            
            # 尝试刷新
            if [ -n "$refresh_token" ]; then
                local tenant_token=$(get_tenant_token)
                local result=$(curl -s "https://open.feishu.cn/open-apis/authen/v1/refresh_access_token" \
                    -H "Authorization: Bearer $tenant_token" \
                    -H "Content-Type: application/json" \
                    -d "{\"grant_type\":\"refresh_token\",\"refresh_token\":\"$refresh_token\"}")
                
                local code_check=$(echo "$result" | jq -r '.code // -1')
                if [ "$code_check" = "0" ]; then
                    local new_access=$(echo "$result" | jq -r '.data.access_token')
                    local new_refresh=$(echo "$result" | jq -r '.data.refresh_token')
                    local expires_in=$(echo "$result" | jq -r '.data.expires_in')
                    local user_name=$(echo "$token_data" | jq -r '.user_name')
                    
                    # 更新存储
                    local temp_file=$(mktemp)
                    cat "$AUTHORIZED_USERS_FILE" | jq --arg id "$user_open_id" \
                        --arg at "$new_access" \
                        --arg rt "$new_refresh" \
                        --argjson exp "$((now + expires_in))" \
                        --arg name "$user_name" \
                        '.[$id] = {
                            "access_token": $at,
                            "refresh_token": $rt,
                            "expires_at": $exp,
                            "user_name": $name,
                            "updated_at": (now | todate)
                        }' > "$temp_file"
                    mv "$temp_file" "$AUTHORIZED_USERS_FILE"
                    
                    echo "$new_access"
                    return 0
                fi
            fi
        fi
    fi
    
    # 兼容旧的 token 文件
    if [ -f "$TOKEN_FILE" ]; then
        local token_data=$(cat "$TOKEN_FILE")
        local saved_open_id=$(echo "$token_data" | jq -r '.user_open_id // empty')
        
        if [ "$saved_open_id" = "$user_open_id" ] || [ -z "$user_open_id" ]; then
            local access_token=$(echo "$token_data" | jq -r '.access_token // empty')
            local expires_at=$(echo "$token_data" | jq -r '.expires_at // 0')
            local refresh_token=$(echo "$token_data" | jq -r '.refresh_token // empty')
            local now=$(date +%s)
            
            if [ -n "$access_token" ] && [ "$expires_at" -gt "$((now + 300))" ]; then
                echo "$access_token"
                return 0
            fi
            
            if [ -n "$refresh_token" ]; then
                local tenant_token=$(get_tenant_token)
                local result=$(curl -s "https://open.feishu.cn/open-apis/authen/v1/refresh_access_token" \
                    -H "Authorization: Bearer $tenant_token" \
                    -H "Content-Type: application/json" \
                    -d "{\"grant_type\":\"refresh_token\",\"refresh_token\":\"$refresh_token\"}")
                
                local code_check=$(echo "$result" | jq -r '.code // -1')
                if [ "$code_check" = "0" ]; then
                    local new_access=$(echo "$result" | jq -r '.data.access_token')
                    local new_refresh=$(echo "$result" | jq -r '.data.refresh_token')
                    local expires_in=$(echo "$result" | jq -r '.data.expires_in')
                    local user_name=$(cat "$TOKEN_FILE" | jq -r '.user_name')
                    
                    cat > "$TOKEN_FILE" << EOF
{
    "user_open_id": "$user_open_id",
    "user_name": "$user_name",
    "access_token": "$new_access",
    "refresh_token": "$new_refresh",
    "expires_at": $((now + expires_in)),
    "created_at": "$(date -Iseconds)"
}
EOF
                    echo "$new_access"
                    return 0
                fi
            fi
        fi
    fi
    
    echo "❌ 需要授权，请运行: oauth.sh generate-auth $user_open_id" >&2
    exit 1
}

# 获取用户主日历
get_primary_calendar() {
    local user_open_id="${1:-$DEFAULT_USER_OPEN_ID}"
    local user_token=$(get_valid_user_token "$user_open_id")
    
    local result=$(curl -s "https://open.feishu.cn/open-apis/calendar/v4/calendars" \
        -H "Authorization: Bearer $user_token")
    
    local code=$(echo "$result" | jq -r '.code // -1')
    if [ "$code" != "0" ]; then
        echo "❌ 获取日历失败: $(echo "$result" | jq -r '.msg')"
        exit 1
    fi
    
    echo "$result" | jq '.data.calendar_list[] | select(.type == "primary") | {calendar_id, summary, type}'
}

# 查询会议室列表
list_rooms() {
    local tenant_token=$(get_tenant_token)
    
    local buildings=$(curl -s "https://open.feishu.cn/open-apis/meeting_room/building/list" \
        -H "Authorization: Bearer $tenant_token")
    
    local building_id=$(echo "$buildings" | jq -r '.data.buildings[0].building_id // empty')
    
    if [ -z "$building_id" ]; then
        echo "❌ 未找到建筑物"
        exit 1
    fi
    
    curl -s -X POST "https://open.feishu.cn/open-apis/meeting_room/room/list" \
        -H "Authorization: Bearer $tenant_token" \
        -H "Content-Type: application/json" \
        -d "{\"building_id\":\"$building_id\"}" | jq '.data.rooms[] | {room_id, name, capacity, floor_name}'
}

# 创建日程事件
create_event() {
    local user_open_id="${1:-$DEFAULT_USER_OPEN_ID}"
    local summary="$2"
    local start_ts="$3"
    local end_ts="$4"
    
    if [ -z "$summary" ] || [ -z "$start_ts" ] || [ -z "$end_ts" ]; then
        echo "用法: $0 create-event [user_open_id] <summary> <start_timestamp> <end_timestamp>"
        exit 1
    fi
    
    local user_token=$(get_valid_user_token "$user_open_id")
    local calendar_id=$(curl -s "https://open.feishu.cn/open-apis/calendar/v4/calendars" \
        -H "Authorization: Bearer $user_token" | jq -r '.data.calendar_list[] | select(.type == "primary") | .calendar_id' | head -1)
    
    if [ -z "$calendar_id" ]; then
        echo "❌ 未找到主日历"
        exit 1
    fi
    
    local result=$(curl -s -X POST "https://open.feishu.cn/open-apis/calendar/v4/calendars/${calendar_id}/events" \
        -H "Authorization: Bearer $user_token" \
        -H "Content-Type: application/json" \
        -d "{\"summary\":\"$summary\",\"start_time\":{\"timestamp\":\"$start_ts\"},\"end_time\":{\"timestamp\":\"$end_ts\"}}")
    
    local code=$(echo "$result" | jq -r '.code // -1')
    if [ "$code" != "0" ]; then
        echo "❌ 创建事件失败: $(echo "$result" | jq -r '.msg')"
        exit 1
    fi
    
    echo "✅ 事件创建成功"
    echo "$result" | jq '.data.event'
}

# 查询日程事件
list_events() {
    local user_open_id="${1:-$DEFAULT_USER_OPEN_ID}"
    local start_ts="$2"
    local end_ts="$3"
    
    local user_token=$(get_valid_user_token "$user_open_id")
    local calendar_id=$(curl -s "https://open.feishu.cn/open-apis/calendar/v4/calendars" \
        -H "Authorization: Bearer $user_token" | jq -r '.data.calendar_list[] | select(.type == "primary") | .calendar_id' | head -1)
    
    curl -s "https://open.feishu.cn/open-apis/calendar/v4/calendars/${calendar_id}/events?start_time=$start_ts&end_time=$end_ts" \
        -H "Authorization: Bearer $user_token" | jq '.data.events[] | {event_id, summary, start_time, end_time}'
}

# 修改日程事件
update_event() {
    local user_open_id="${1:-$DEFAULT_USER_OPEN_ID}"
    local event_id="$2"
    local summary="$3"
    local start_ts="$4"
    local end_ts="$5"
    
    local user_token=$(get_valid_user_token "$user_open_id")
    local calendar_id=$(curl -s "https://open.feishu.cn/open-apis/calendar/v4/calendars" \
        -H "Authorization: Bearer $user_token" | jq -r '.data.calendar_list[] | select(.type == "primary") | .calendar_id' | head -1)
    
    local body="{}"
    [ -n "$summary" ] && body=$(echo "$body" | jq --arg s "$summary" '. + {summary: $s}')
    [ -n "$start_ts" ] && body=$(echo "$body" | jq --arg t "$start_ts" '. + {start_time: {timestamp: $t}}')
    [ -n "$end_ts" ] && body=$(echo "$body" | jq --arg t "$end_ts" '. + {end_time: {timestamp: $t}}')
    
    curl -s -X PATCH "https://open.feishu.cn/open-apis/calendar/v4/calendars/${calendar_id}/events/${event_id}" \
        -H "Authorization: Bearer $user_token" \
        -H "Content-Type: application/json" \
        -d "$body" | jq '.'
}

# 删除日程事件
delete_event() {
    local user_open_id="${1:-$DEFAULT_USER_OPEN_ID}"
    local event_id="$2"
    
    local user_token=$(get_valid_user_token "$user_open_id")
    local calendar_id=$(curl -s "https://open.feishu.cn/open-apis/calendar/v4/calendars" \
        -H "Authorization: Bearer $user_token" | jq -r '.data.calendar_list[] | select(.type == "primary") | .calendar_id' | head -1)
    
    curl -s -X DELETE "https://open.feishu.cn/open-apis/calendar/v4/calendars/${calendar_id}/events/${event_id}" \
        -H "Authorization: Bearer $user_token" | jq '.'
}

# 预约会议室
reserve_room() {
    local user_open_id="${1:-$DEFAULT_USER_OPEN_ID}"
    local room_id="$2"
    local start_ts="$3"
    local end_ts="$4"
    local event_id="$5"
    
    local user_token=$(get_valid_user_token "$user_open_id")
    
    local body="{\"room_ids\":[\"$room_id\"],\"start_time\":\"$start_ts\",\"end_time\":\"$end_ts\""
    [ -n "$event_id" ] && body=$(echo "$body" | jq --arg e "$event_id" '. + {event_id: $e}')
    
    curl -s -X POST "https://open.feishu.cn/open-apis/meeting_room/room/reserve" \
        -H "Authorization: Bearer $user_token" \
        -H "Content-Type: application/json" \
        -d "$body" | jq '.'
}

# 完整预约流程（创建事件 + 预约会议室）
book_meeting() {
    local user_open_id="${1:-$DEFAULT_USER_OPEN_ID}"
    local summary="$2"
    local start_ts="$3"
    local end_ts="$4"
    local room_id="$5"
    
    if [ -z "$summary" ] || [ -z "$start_ts" ] || [ -z "$end_ts" ] || [ -z "$room_id" ]; then
        echo "用法: $0 book-meeting [user_open_id] <summary> <start_timestamp> <end_timestamp> <room_id>"
        exit 1
    fi
    
    echo "📅 正在创建日程事件..."
    local user_token=$(get_valid_user_token "$user_open_id")
    local calendar_id=$(curl -s "https://open.feishu.cn/open-apis/calendar/v4/calendars" \
        -H "Authorization: Bearer $user_token" | jq -r '.data.calendar_list[] | select(.type == "primary") | .calendar_id' | head -1)
    
    local event_result=$(curl -s -X POST "https://open.feishu.cn/open-apis/calendar/v4/calendars/${calendar_id}/events" \
        -H "Authorization: Bearer $user_token" \
        -H "Content-Type: application/json" \
        -d "{\"summary\":\"$summary\",\"start_time\":{\"timestamp\":\"$start_ts\"},\"end_time\":{\"timestamp\":\"$end_ts\"}}")
    
    local event_id=$(echo "$event_result" | jq -r '.data.event.event_id // empty')
    
    if [ -z "$event_id" ]; then
        echo "❌ 创建事件失败"
        echo "$event_result" | jq '.'
        exit 1
    fi
    
    echo "✅ 事件创建成功: $event_id"
    
    echo "🚪 正在预约会议室..."
    local reserve_result=$(curl -s -X POST "https://open.feishu.cn/open-apis/meeting_room/room/reserve" \
        -H "Authorization: Bearer $user_token" \
        -H "Content-Type: application/json" \
        -d "{\"room_ids\":[\"$room_id\"],\"start_time\":\"$start_ts\",\"end_time\":\"$end_ts\",\"event_id\":\"$event_id\"}")
    
    local reserve_code=$(echo "$reserve_result" | jq -r '.code // -1')
    
    if [ "$reserve_code" = "0" ]; then
        echo "✅ 会议室预约成功！"
        echo ""
        echo "📋 会议信息:"
        echo "   主题: $summary"
        echo "   时间: $(date -d @$start_ts '+%Y-%m-%d %H:%M') - $(date -d @$end_ts '+%H:%M')"
        echo "   事件ID: $event_id"
    else
        echo "⚠️ 会议室预约失败，日程已创建"
        echo "$reserve_result" | jq '.'
    fi
}

# 智能预约（从自然语言解析）
smart_book() {
    local user_open_id="${1:-$DEFAULT_USER_OPEN_ID}"
    local room_name="$2"
    local time_desc="$3"
    local summary="$4"
    
    # 解析会议室名称
    local room_id=$(list_rooms | jq -r --arg name "$room_name" 'select(.name | contains($name)) | .room_id' | head -1)
    
    if [ -z "$room_id" ]; then
        echo "❌ 未找到会议室: $room_name"
        list_rooms
        exit 1
    fi
    
    # 解析时间（简化版，需要更完善的 NLP）
    local start_ts end_ts
    
    case "$time_desc" in
        *明天*下午*|*tomorrow*afternoon*)
            local hour=$(echo "$time_desc" | grep -oP '\d+(?=点|:)' | head -1)
            hour=${hour:-15}
            start_ts=$(date -d "tomorrow ${hour}:00:00 Asia/Shanghai" +%s)
            end_ts=$((start_ts + 3600))
            ;;
        *)
            echo "❌ 暂不支持的时间格式: $time_desc"
            echo "支持格式: 明天下午3点"
            exit 1
            ;;
    esac
    
    echo "📍 会议室: $room_name ($room_id)"
    echo "🕐 时间: $(date -d @$start_ts '+%Y-%m-%d %H:%M') - $(date -d @$end_ts '+%H:%M')"
    echo "📝 主题: $summary"
    echo ""
    
    book_meeting "$user_open_id" "$summary" "$start_ts" "$end_ts" "$room_id"
}

# 帮助
show_help() {
    cat << EOF
飞书日历和会议室操作工具（自动化版本）

用法:
    $0 get-primary-calendar [user_open_id]
    $0 list-rooms
    $0 create-event [user_open_id] <summary> <start> <end>
    $0 list-events [user_open_id] <start> <end>
    $0 update-event [user_open_id] <event_id> [summary] [start] [end]
    $0 delete-event [user_open_id] <event_id>
    $0 reserve-room [user_open_id] <room_id> <start> <end> [event_id]
    $0 book-meeting [user_open_id] <summary> <start> <end> <room_id>
    $0 smart-book [user_open_id] <room_name> <time_desc> <summary>

智能预约示例:
    $0 smart-book 1910 "明天下午3点" "测试会议"

时间戳格式: Unix timestamp (秒)
默认用户: $DEFAULT_USER_OPEN_ID
EOF
}

# 主入口
case "${1:-}" in
    get-primary-calendar)
        get_primary_calendar "$2"
        ;;
    list-rooms)
        list_rooms
        ;;
    create-event)
        create_event "$2" "$3" "$4" "$5"
        ;;
    list-events)
        list_events "$2" "$3" "$4"
        ;;
    update-event)
        update_event "$2" "$3" "$4" "$5" "$6"
        ;;
    delete-event)
        delete_event "$2" "$3"
        ;;
    reserve-room)
        reserve_room "$2" "$3" "$4" "$5" "$6"
        ;;
    book-meeting)
        book_meeting "$2" "$3" "$4" "$5" "$6"
        ;;
    smart-book)
        smart_book "$2" "$3" "$4" "$5"
        ;;
    *)
        show_help
        ;;
esac
