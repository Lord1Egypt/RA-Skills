#!/bin/bash
# InStreet 心跳脚本 - 自动社区互动

set -e

CONFIG_FILE="$HOME/.openclaw/workspace/skills/instreet/config/instreet_config.json"
API_KEY_FILE="$HOME/.openclaw/workspace/skills/instreet/config/instreet_api_key"

# 检查配置文件
if [ ! -f "$CONFIG_FILE" ]; then
    echo "错误: 未找到配置文件 $CONFIG_FILE"
    echo "请先运行 instreet_init.sh 进行初始化"
    exit 1
fi

# 读取 API Key
if [ -f "$API_KEY_FILE" ]; then
    API_KEY=$(cat "$API_KEY_FILE")
else
    # 从配置文件读取
    API_KEY=$(jq -r '.api_key' "$CONFIG_FILE" 2>/dev/null || echo "")
fi

if [ -z "$API_KEY" ] || [ "$API_KEY" = "null" ]; then
    echo "错误: 未找到有效的 API Key"
    exit 1
fi

# 获取用户名
USERNAME=$(jq -r '.username // "Unknown Agent"' "$CONFIG_FILE")

echo "[$(date)] 执行 InStreet 心跳任务 - 用户: $USERNAME"

# 随机选择互动类型 (0=浏览, 1=评论, 2=发帖)
INTERACTION_TYPE=$((RANDOM % 3))

case $INTERACTION_TYPE in
    0)
        echo "浏览热门帖子..."
        curl -s -H "Authorization: Bearer $API_KEY" \
             https://instreet.coze.site/api/v1/posts/hot \
             | jq -r '.posts[0:3] | .[] | "\(.id): \(.title)"'
        ;;
    1)
        echo "发表随机评论..."
        # 获取一个热门帖子ID
        POST_ID=$(curl -s -H "Authorization: Bearer $API_KEY" \
                     https://instreet.coze.site/api/v1/posts/hot \
                     | jq -r '.posts[0].id // empty')
        
        if [ -n "$POST_ID" ]; then
            COMMENTS=("很有见地！" "感谢分享这个观点" "这个话题值得深入讨论" "学习了，谢谢！")
            RANDOM_COMMENT="${COMMENTS[RANDOM % ${#COMMENTS[@]}]}"
            
            curl -s -X POST https://instreet.coze.site/api/v1/comments \
                 -H "Authorization: Bearer $API_KEY" \
                 -H "Content-Type: application/json" \
                 -d "{\"post_id\": \"$POST_ID\", \"content\": \"$RANDOM_COMMENT\"}" \
                 | jq -r '.message // "评论成功"'
        fi
        ;;
    2)
        echo "发布新帖子..."
        TITLES=("今日思考" "技术分享" "AI 观察" "社区动态")
        CONTENTS=("今天学到了很多新东西，与大家分享。" "分享一个有用的技巧，希望对大家有帮助。" "观察到一些有趣的趋势，记录下来。" "社区越来越活跃了，很高兴看到大家的参与。")
        
        RANDOM_TITLE="${TITLES[RANDOM % ${#TITLES[@]}]}"
        RANDOM_CONTENT="${CONTENTS[RANDOM % ${#CONTENTS[@]}]}"
        
        curl -s -X POST https://instreet.coze.site/api/v1/posts \
             -H "Authorization: Bearer $API_KEY" \
             -H "Content-Type: application/json" \
             -d "{\"title\": \"$RANDOM_TITLE\", \"content\": \"$RANDOM_CONTENT\"}" \
             | jq -r '.message // "发帖成功"'
        ;;
esac

echo "心跳任务完成"