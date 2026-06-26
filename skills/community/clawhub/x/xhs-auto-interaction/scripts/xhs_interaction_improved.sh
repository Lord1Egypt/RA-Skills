#!/bin/bash

# 小红书互动脚本（改进版）
# 1. 避免重复操作已互动过的笔记
# 2. 扩展搜索关键词范围
# 3. 智能错误处理和状态判断
# 4. 记录操作历史，避免重复
# 5. 更好的xsec_token处理

set -e

MCP_URL="http://localhost:18060/mcp"
LOG_FILE="/home/chan/.openclaw/workspace/xhs_interaction_improved.log"
HISTORY_FILE="/home/chan/.openclaw/workspace/xhs_interaction_history.txt"

# 扩展的搜索关键词数组 - 新加坡私立大学相关内容
KEYWORDS=(
    "新加坡留学"
    "新加坡私立大学"
    "新加坡管理学院"
    "新加坡楷博高等教育学院"
    "新加坡PSB学院"
    "新加坡东亚管理学院"
    "新加坡留学咨询"
    "新加坡本科留学"
    "新加坡硕士留学"
    "新加坡留学费用"
    "新加坡留学申请"
    "新加坡留学条件"
    "新加坡留学签证"
    "新加坡留学优势"
    "新加坡留学就业"
)

# 随机选择一个关键词
RANDOM_INDEX=$((RANDOM % ${#KEYWORDS[@]}))
KEYWORD="${KEYWORDS[$RANDOM_INDEX]}"

echo "=== 小红书互动脚本（改进版）开始执行 $(date '+%Y-%m-%d %H:%M:%S') ===" | tee -a "$LOG_FILE"
echo "📌 本次搜索关键词: $KEYWORD" | tee -a "$LOG_FILE"

# 初始化MCP会话
echo "1. 初始化MCP会话..." | tee -a "$LOG_FILE"
SESSION_ID=$(curl -s -D /tmp/xhs_headers -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"openclaw","version":"1.0"}},"id":1}' > /dev/null && grep -i 'Mcp-Session-Id' /tmp/xhs_headers | tr -d '\r' | awk '{print $2}')

if [ -z "$SESSION_ID" ]; then
    echo "❌ 初始化失败：无法获取SESSION_ID" | tee -a "$LOG_FILE"
    exit 1
fi
echo "✅ 获取SESSION_ID: ${SESSION_ID:0:20}..." | tee -a "$LOG_FILE"

# 发送initialized通知
echo "2. 发送initialized通知..." | tee -a "$LOG_FILE"
curl -s -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}' > /dev/null

# 检查登录状态
echo "3. 检查登录状态..." | tee -a "$LOG_FILE"
LOGIN_RESULT=$(curl -s -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"check_login_status","arguments":{}},"id":2}' | jq -r '.result.content[0].text // "未知"')

echo "登录状态: $LOGIN_RESULT" | tee -a "$LOG_FILE"

# 搜索内容
echo "4. 搜索内容: $KEYWORD..." | tee -a "$LOG_FILE"
SEARCH_RESULT=$(curl -s -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"search_feeds","arguments":{"keyword":"'"$KEYWORD"'"}},"id":3}')

# 提取搜索结果
echo "5. 提取搜索结果..." | tee -a "$LOG_FILE"
FEEDS_JSON=$(echo "$SEARCH_RESULT" | jq -r '.result.content[0].text')
FEED_COUNT=$(echo "$FEEDS_JSON" | jq -r '.feeds | length')

if [ "$FEED_COUNT" -eq 0 ]; then
    echo "❌ 搜索失败：未找到相关内容" | tee -a "$LOG_FILE"
    exit 1
fi

echo "✅ 找到 $FEED_COUNT 个相关内容" | tee -a "$LOG_FILE"

# 浏览推荐内容
echo "6. 浏览推荐内容..." | tee -a "$LOG_FILE"
BROWSE_RESULT=$(curl -s -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"list_feeds","arguments":{}},"id":4}' | jq -r '.result.content[0].text // "浏览完成"')

echo "浏览结果: $BROWSE_RESULT" | tee -a "$LOG_FILE"

# 加载历史记录
declare -A LIKED_HISTORY
declare -A FAVORITED_HISTORY

if [ -f "$HISTORY_FILE" ]; then
    echo "📖 加载历史记录..." | tee -a "$LOG_FILE"
    while IFS= read -r line; do
        if [[ "$line" =~ ^LIKE:([^:]+):(.+)$ ]]; then
            LIKED_HISTORY["${BASH_REMATCH[1]}"]="${BASH_REMATCH[2]}"
        elif [[ "$line" =~ ^FAVORITE:([^:]+):(.+)$ ]]; then
            FAVORITED_HISTORY["${BASH_REMATCH[1]}"]="${BASH_REMATCH[2]}"
        fi
    done < "$HISTORY_FILE"
    echo "📊 历史记录：已点赞 ${#LIKED_HISTORY[@]} 篇，已收藏 ${#FAVORITED_HISTORY[@]} 篇" | tee -a "$LOG_FILE"
fi

# 智能互动处理
LIKE_COUNT=0
FAVORITE_COUNT=0
SKIP_COUNT=0
PROCESSED_COUNT=0
MAX_ATTEMPTS=10  # 最多尝试10个内容

echo "7. 开始智能互动操作..." | tee -a "$LOG_FILE"

for i in $(seq 0 $((MAX_ATTEMPTS-1))); do
    if [ $i -ge $FEED_COUNT ]; then
        break
    fi
    
    # 使用jq直接提取笔记信息
    FEED_INFO=$(echo "$FEEDS_JSON" | jq -r ".feeds[$i]")
    FEED_ID=$(echo "$FEED_INFO" | jq -r '.id // empty')
    XSEC_TOKEN=$(echo "$FEED_INFO" | jq -r '.xsecToken // empty')
    TITLE=$(echo "$FEED_INFO" | jq -r '.noteCard.displayTitle // "无标题"')
    AUTHOR=$(echo "$FEED_INFO" | jq -r '.noteCard.user.nickname // "未知作者"')
    
    if [ -z "$FEED_ID" ] || [ -z "$XSEC_TOKEN" ]; then
        echo "⚠️ 跳过第 $((i+1)) 个结果：缺少feed_id或xsec_token" | tee -a "$LOG_FILE"
        SKIP_COUNT=$((SKIP_COUNT + 1))
        continue
    fi
    
    PROCESSED_COUNT=$((PROCESSED_COUNT + 1))
    echo "处理第 $((i+1)) 个内容: $TITLE (作者: $AUTHOR)" | tee -a "$LOG_FILE"
    echo "  Feed ID: $FEED_ID" | tee -a "$LOG_FILE"
    
    # 检查是否已经点赞过
    if [ -n "${LIKED_HISTORY[$FEED_ID]}" ]; then
        echo "  ℹ️ 已点赞过（历史记录: ${LIKED_HISTORY[$FEED_ID]}），跳过点赞" | tee -a "$LOG_FILE"
    else
        # 执行点赞
        echo "  执行点赞..." | tee -a "$LOG_FILE"
        LIKE_RESPONSE=$(curl -s -X POST "$MCP_URL" \
          -H "Content-Type: application/json" \
          -H "Mcp-Session-Id: $SESSION_ID" \
          -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"like_feed","arguments":{"feed_id":"'"$FEED_ID"'","xsec_token":"'"$XSEC_TOKEN"'"}},"id":5}')
        
        LIKE_RESULT=$(echo "$LIKE_RESPONSE" | jq -r '.result.content[0].text // "未知错误"')
        
        if echo "$LIKE_RESULT" | grep -q "点赞成功"; then
            echo "  ✅ 点赞成功！" | tee -a "$LOG_FILE"
            LIKE_COUNT=$((LIKE_COUNT + 1))
            # 记录到历史
            echo "LIKE:$FEED_ID:$(date '+%Y-%m-%d %H:%M:%S')" >> "$HISTORY_FILE"
        elif echo "$LIKE_RESULT" | grep -q "已经点过赞\|已点赞\|点赞失败" ; then
            echo "  ℹ️ 点赞状态: $LIKE_RESULT" | tee -a "$LOG_FILE"
            # 即使失败也记录，避免重复尝试
            echo "LIKE:$FEED_ID:$(date '+%Y-%m-%d %H:%M:%S')_failed" >> "$HISTORY_FILE"
        elif echo "$LIKE_RESULT" | grep -q "not in noteDetailMap\|context deadline exceeded\|panic="; then
            echo "  ⚠️ MCP服务错误: 笔记详情缺失或超时，跳过此笔记" | tee -a "$LOG_FILE"
            echo "LIKE:$FEED_ID:$(date '+%Y-%m-%d %H:%M:%S')_mcp_error" >> "$HISTORY_FILE"
        else
            echo "  ⚠️ 点赞失败: $LIKE_RESULT" | tee -a "$LOG_FILE"
        fi
    fi
    
    # 短暂等待
    sleep 1
    
    # 检查是否已经收藏过
    if [ -n "${FAVORITED_HISTORY[$FEED_ID]}" ]; then
        echo "  ℹ️ 已收藏过（历史记录: ${FAVORITED_HISTORY[$FEED_ID]}），跳过收藏" | tee -a "$LOG_FILE"
    else
        # 执行收藏
        echo "  执行收藏..." | tee -a "$LOG_FILE"
        FAVORITE_RESPONSE=$(curl -s -X POST "$MCP_URL" \
          -H "Content-Type: application/json" \
          -H "Mcp-Session-Id: $SESSION_ID" \
          -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"favorite_feed","arguments":{"feed_id":"'"$FEED_ID"'","xsec_token":"'"$XSEC_TOKEN"'"}},"id":6}')
        
        FAVORITE_RESULT=$(echo "$FAVORITE_RESPONSE" | jq -r '.result.content[0].text // "未知错误"')
        
        if echo "$FAVORITE_RESULT" | grep -q "收藏成功"; then
            echo "  ✅ 收藏成功！" | tee -a "$LOG_FILE"
            FAVORITE_COUNT=$((FAVORITE_COUNT + 1))
            # 记录到历史
            echo "FAVORITE:$FEED_ID:$(date '+%Y-%m-%d %H:%M:%S')" >> "$HISTORY_FILE"
        elif echo "$FAVORITE_RESULT" | grep -q "已经收藏过\|已收藏\|收藏失败" ; then
            echo "  ℹ️ 收藏状态: $FAVORITE_RESULT" | tee -a "$LOG_FILE"
            # 即使失败也记录，避免重复尝试
            echo "FAVORITE:$FEED_ID:$(date '+%Y-%m-%d %H:%M:%S')_failed" >> "$HISTORY_FILE"
        elif echo "$FAVORITE_RESULT" | grep -q "not in noteDetailMap\|context deadline exceeded\|panic="; then
            echo "  ⚠️ MCP服务错误: 笔记详情缺失或超时，跳过此笔记" | tee -a "$LOG_FILE"
            echo "FAVORITE:$FEED_ID:$(date '+%Y-%m-%d %H:%M:%S')_mcp_error" >> "$HISTORY_FILE"
        else
            echo "  ⚠️ 收藏失败: $FAVORITE_RESULT" | tee -a "$LOG_FILE"
        fi
    fi
    
    # 短暂等待，避免请求过快
    sleep 2
done

echo "=== 智能互动操作完成 ===" | tee -a "$LOG_FILE"
echo "📊 执行统计：" | tee -a "$LOG_FILE"
echo "  搜索关键词: $KEYWORD" | tee -a "$LOG_FILE"
echo "  找到内容数: $FEED_COUNT" | tee -a "$LOG_FILE"
echo "  尝试处理数: $MAX_ATTEMPTS" | tee -a "$LOG_FILE"
echo "  实际处理数: $PROCESSED_COUNT" | tee -a "$LOG_FILE"
echo "  跳过内容数: $SKIP_COUNT" | tee -a "$LOG_FILE"
echo "  成功点赞数: $LIKE_COUNT" | tee -a "$LOG_FILE"
echo "  成功收藏数: $FAVORITE_COUNT" | tee -a "$LOG_FILE"
echo "  浏览内容: 已完成" | tee -a "$LOG_FILE"
echo "  历史记录: 已保存到 $HISTORY_FILE" | tee -a "$LOG_FILE"

# 显示点赞的笔记链接
echo -e "\n🎯 本次点赞的笔记链接：" | tee -a "$LOG_FILE"
if [ -f "$HISTORY_FILE" ]; then
    grep "^LIKE:$FEED_ID:" "$HISTORY_FILE" | tail -$LIKE_COUNT | while read -r line; do
        if [[ "$line" =~ ^LIKE:([^:]+): ]]; then
            feed_id="${BASH_REMATCH[1]}"
            echo "  🔗 https://www.xiaohongshu.com/explore/$feed_id" | tee -a "$LOG_FILE"
        fi
    done
fi

echo "=== 脚本执行结束 $(date '+%Y-%m-%d %H:%M:%S') ===" | tee -a "$LOG_FILE"