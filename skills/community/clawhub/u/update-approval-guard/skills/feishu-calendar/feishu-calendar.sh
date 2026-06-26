#!/bin/bash
# Feishu Calendar Helper Script
# 飞书日历辅助脚本

set -e

# 配置
APP_ID="cli_a92fba8c65e35cc4"
APP_SECRET="UFUvM2wNSkErIxe7t63ZrgyecakLwNQR"
REDIRECT_URI="https://open.feishu.cn/open-apis/authen/v1/index"

# 存储路径
CREDENTIALS_DIR="/root/.openclaw/credentials"
USER_TOKEN_FILE="$CREDENTIALS_DIR/feishu-user-token.json"

# 获取 tenant_access_token
get_tenant_token() {
    curl -s "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
        -H "Content-Type: application/json" \
        -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" | jq -r '.tenant_access_token'
}

# 获取 user_access_token (需要先授权)
get_user_token() {
    if [ -f "$USER_TOKEN_FILE" ]; then
        local token_data=$(cat "$USER_TOKEN_FILE")
        local expires_at=$(echo "$token_data" | jq -r '.expires_at // 1000')
        local now=$(date +%s)
        
        # 检查是否过期
        if [ "$expires_at" -gt "$now" ]; then
            echo "$token_data" | jq -r '.access_token'
            return 0
        fi
        
        # 尝试刷新 token
        local refresh_token=$(echo "$token_data" | jq -r '.refresh_token')
        local new_token=$(curl -s "https://open.feishu.cn/open-apis/authen/v1/refresh_access_token" \
            -H "Content-Type: application/json" \
            -d "{\"grant_type\":\"refresh_token\",\"refresh_token\":\"$refresh_token\"}" | jq -r '.data.access_token')
        
        if [ -n "$new_token" ] && [ "$new_token" != "null" ]; then
            echo "$new_token"
            return 0
        fi
    fi
    echo ""
    return 1
}

# 生成授权链接
generate_auth_url() {
    local state=$(openssl rand -hex 16 2>/dev/null || echo "random_state_$$")
    echo "https://open.feishu.cn/open-apis/authen/v1/authorize?app_id=$APP_ID&redirect_uri=$REDIRECT_URI&state=$state"
}

# 保存用户授权
save_user_token() {
    local code="$1"
    if [ -z "$code" ]; then
        echo "Usage: $0 save-user-token <code>"
        return 1
    fi
    
    local token_data=$(curl -s "https://open.feishu.cn/open-apis/authen/v1/access_token" \
        -H "Content-Type: application/json" \
        -d "{\"grant_type\":\"authorization_code\",\"code\":\"$code\"}")
    
    echo "$token_data" > "$USER_TOKEN_FILE"
    echo "User token saved"
}

# 获取用户主日历
get_primary_calendar() {
    local user_token=$(get_user_token)
    if [ -z "$user_token" ]; then
        echo "Error: User not authorized. Please run generate-auth-url first."
        return 1
    fi
    
    curl -s "https://open.feishu.cn/open-apis/calendar/v4/calendars" \
        -H "Authorization: Bearer $user_token" | jq '.data.calendar_list[] | select(.type == "primary") | {calendar_id, summary}'
}

# 创建日程事件
create_event() {
    local summary="$1"
    local start_time="$2"
    local end_time="$3"
    local attendees="$4"
    local room_id="$5"
    
    local user_token=$(get_user_token)
    if [ -z "$user_token" ]; then
        echo "Error: User not authorized"
        return 1
    fi
    
    # 获取用户主日历
    local calendar_id=$(curl -s "https://open.feishu.cn/open-apis/calendar/v4/calendars" \
        -H "Authorization: Bearer $user_token" | jq -r '.data.calendar_list[] | select(.type == "primary") | .calendar_id' | head -1)
    
    # 构建请求体
    local request_body=$(jq -n \
        --arg summary "$summary" \
        --arg start "$start_time" \
        --arg end "$end_time" \
        '{"summary":$summary,"start_time":{"timestamp":$start},"end_time":{"timestamp":$end}}')
    
    # 创建事件
    local event_result=$(curl -s -X POST "https://open.feishu.cn/open-apis/calendar/v4/calendars/${calendar_id}/events" \
        -H "Authorization: Bearer $user_token" \
        -H "Content-Type: application/json" \
        -d "$request_body")
    
    local event_id=$(echo "$event_result" | jq -r '.data.event.event_id')
    
    # 添加参会者
    if [ -n "$attendees" ] && [ "$attendees" != "null" ]; then
        curl -s -X POST "https://open.feishu.cn/open-apis/calendar/v4/calendars/${calendar_id}/events/${event_id}/attendees" \
            -H "Authorization: Bearer $user_token" \
            -H "Content-Type: application/json" \
            -d "{\"attendees\":$attendees}" > /dev/null
    fi
    
    # 预约会议室
    if [ -n "$room_id" ] && [ "$room_id" != "null" ]; then
        curl -s -X POST "https://open.feishu.cn/open-apis/meeting_room/room/reserve" \
            -H "Authorization: Bearer $user_token" \
            -H "Content-Type: application/json" \
            -d "{\"room_ids\":[\"$room_id\"],\"start_time\":\"$start_time\",\"end_time\":\"$end_time\",\"event_id\":\"$event_id\"}" > /dev/null
    fi
    
    echo "$event_result" | jq '.'
}

# 查询日程事件
list_events() {
    local start_time="$1"
    local end_time="$2"
    
    local user_token=$(get_user_token)
    if [ -z "$user_token" ]; then
        echo "Error: User not authorized"
        return 1
    fi
    
    local calendar_id=$(curl -s "https://open.feishu.cn/open-apis/calendar/v4/calendars" \
        -H "Authorization: Bearer $user_token" | jq -r '.data.calendar_list[] | select(.type == "primary") | .calendar_id' | head -1)
    
    curl -s "https://open.feishu.cn/open-apis/calendar/v4/calendars/${calendar_id}/events?start_time=$start_time&end_time=$end_time" \
        -H "Authorization: Bearer $user_token" | jq '.data.events[] | {event_id, summary, start_time, end_time}'
}

# 修改日程事件
update_event() {
    local event_id="$1"
    local summary="$2"
    local start_time="$3"
    local end_time="$4"
    
    local user_token=$(get_user_token)
    if [ -z "$user_token" ]; then
        echo "Error: User not authorized"
        return 1
    fi
    
    local calendar_id=$(curl -s "https://open.feishu.cn/open-apis/calendar/v4/calendars" \
        -H "Authorization: Bearer $user_token" | jq -r '.data.calendar_list[] | select(.type == "primary") | .calendar_id' | head -1)
    
    local request_body=$(jq -n \
        --arg summary "$summary" \
        --arg start "$start_time" \
        --arg end "$end_time" \
        '{"summary":$summary,"start_time":{"timestamp":$start},"end_time":{"timestamp":$end}}')
    
    curl -s -X PATCH "https://open.feishu.cn/open-apis/calendar/v4/calendars/${calendar_id}/events/${event_id}" \
        -H "Authorization: Bearer $user_token" \
        -H "Content-Type: application/json" \
        -d "$request_body" | jq '.'
}

# 删除日程事件
delete_event() {
    local event_id="$1"
    
    local user_token=$(get_user_token)
    if [ -z "$user_token" ]; then
        echo "Error: User not authorized"
        return 1
    fi
    
    local calendar_id=$(curl -s "https://open.feishu.cn/open-apis/calendar/v4/calendars" \
        -H "Authorization: Bearer $user_token" | jq -r '.data.calendar_list[] | select(.type == "primary") | .calendar_id' | head -1)
    
    curl -s -X DELETE "https://open.feishu.cn/open-apis/calendar/v4/calendars/${calendar_id}/events/${event_id}" \
        -H "Authorization: Bearer $user_token" | jq '.'
}

# 获取会议室列表
list_rooms() {
    local tenant_token=$(get_tenant_token)
    
    # 获取建筑物列表
    local building_id=$(curl -s "https://open.feishu.cn/open-apis/meeting_room/building/list" \
        -H "Authorization: Bearer $tenant_token" | jq -r '.data.buildings[0].building_id')
    
    # 获取会议室列表
    curl -s -X POST "https://open.feishu.cn/open-apis/meeting_room/room/list" \
        -H "Authorization: Bearer $tenant_token" \
        -H "Content-Type: application/json" \
        -d "{\"building_id\":\"$building_id\"}" | jq '.data.rooms[] | {room_id, name, capacity, floor_name}'
}

# 预约会议室
reserve_room() {
    local room_id="$1"
    local start_time="$2"
    local end_time="$3"
    local event_id="$4"
    
    local user_token=$(get_user_token)
    if [ -z "$user_token" ]; then
        echo "Error: User not authorized"
        return 1
    fi
    
    curl -s -X POST "https://open.feishu.cn/open-apis/meeting_room/room/reserve" \
        -H "Authorization: Bearer $user_token" \
        -H "Content-Type: application/json" \
        -d "{\"room_ids\":[\"$room_id\"],\"start_time\":\"$start_time\",\"end_time\":\"$end_time\",\"event_id\":\"$event_id\"}" | jq '.'
}

# 帮助信息
show_help() {
    cat << EOF
Feishu Calendar Helper

Commands:
  generate-auth-url     生成用户授权链接
  save-user-token <code>  保存用户授权码
  get-primary-calendar  获取用户主日历
  create-event <summary> <start_timestamp> <end_timestamp> [attendees_json] [room_id]
                        创建日程事件
  list-events <start_timestamp> <end_timestamp>
                        查询日程事件
  update-event <event_id> <summary> <start_timestamp> <end_timestamp>
                        修改日程事件
  delete-event <event_id>
                        删除日程事件
  list-rooms            获取会议室列表
  reserve-room <room_id> <start_time> <end_time> [event_id]
                        预约会议室

Examples:
  # 生成授权链接
  $0 generate-auth-url
  
  # 创建明天9点的会议
  $0 create-event "会议" 1772672400 1772676000
  
  # 查询明天的日程
  $0 list-events 1772624000 1772710400
EOF
}

# 主入口
case "$1" in
    generate-auth-url)
        generate_auth_url
        ;;
    save-user-token)
        save_user_token "$2"
        ;;
    get-primary-calendar)
        get_primary_calendar
        ;;
    create-event)
        create_event "$2" "$3" "$4" "$5" "$6"
        ;;
    list-events)
        list_events "$2" "$3"
        ;;
    update-event)
        update_event "$2" "$3" "$4" "$5"
        ;;
    delete-event)
        delete_event "$2"
        ;;
    list-rooms)
        list_rooms
        ;;
    reserve-room)
        reserve_room "$2" "$3" "$4" "$5"
        ;;
    *)
        show_help
        ;;
esac
