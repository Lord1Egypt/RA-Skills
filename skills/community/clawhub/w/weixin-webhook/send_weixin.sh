#!/bin/bash
# send_weixin.sh - 最终修复版

# 参数检查
if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
    echo "用法: $0 <webhook_key> <msgtype> <content> [mentioned_list] [mentioned_mobile_list]"
    echo "示例: $0 'key' 'text' '消息内容' 'user1,user2' '13800001111,@all'"
    exit 1
fi

# 定义变量
WEBHOOK_KEY="$1"
MSGTYPE="$2"
CONTENT="$3"
MENTIONED_LIST="$4"
MENTIONED_MOBILE_LIST="$5"

# 构建JSON
case "$MSGTYPE" in
    text)
        # 基础text对象 - 注意这里是对象，不加外层{}
        TEXT_OBJ="\"content\":\"$CONTENT\""
        
        # 添加mentioned_list
        if [ -n "$MENTIONED_LIST" ]; then
            MENTIONED_ARRAY=$(echo "$MENTIONED_LIST" | tr ',' '\n' | awk '{print "\""$0"\""}' | paste -sd ',' -)
            TEXT_OBJ="$TEXT_OBJ, \"mentioned_list\":[$MENTIONED_ARRAY]"
        fi
        
        # 添加mentioned_mobile_list
        if [ -n "$MENTIONED_MOBILE_LIST" ]; then
            MOBILE_ARRAY=$(echo "$MENTIONED_MOBILE_LIST" | tr ',' '\n' | awk '{print "\""$0"\""}' | paste -sd ',' -)
            TEXT_OBJ="$TEXT_OBJ, \"mentioned_mobile_list\":[$MOBILE_ARRAY]"
        fi
        
        # 完整JSON：text的值是一个对象{...}
        JSON_DATA="{\"msgtype\":\"text\",\"text\":{$TEXT_OBJ}}"
        ;;
    markdown)
        JSON_DATA="{\"msgtype\":\"markdown\",\"markdown\":{\"content\":\"$CONTENT\"}}"
        ;;
    *)
        echo "不支持的消息类型: $MSGTYPE"
        exit 1
        ;;
esac

# 发送请求
echo "发送的JSON数据：$JSON_DATA"
response=$(curl -s -X POST "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=$WEBHOOK_KEY" \
  -H "Content-Type: application/json" \
  -d "$JSON_DATA")

echo "$response" | jq '.' 2>/dev/null || echo "$response"