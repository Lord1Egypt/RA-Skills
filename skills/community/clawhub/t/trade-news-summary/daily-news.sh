#!/bin/bash

# ============================================================
# 外贸资讯聚合器（最终确定版）
# 版本：2.2.3
# ============================================================

RSS_FEEDS=${RSS_FEEDS:-"https://www.bing.com/news/search?q=hat&format=rss,https://www.bing.com/news/search?q=textile&format=rss,https://www.bing.com/news/search?q=shipping&format=rss,https://www.bing.com/news/search?q=tariff&format=rss,https://www.bing.com/news/search?q=ecommerce&format=rss"}
KEYWORDS=${KEYWORDS:-}
MAX_ITEMS=${MAX_ITEMS:-30}
INCLUDE_HACKER_NEWS=${INCLUDE_HACKER_NEWS:-false}
BAIDU_APPID=${BAIDU_APPID:-}
BAIDU_SECRET=${BAIDU_SECRET:-}
FEISHU_WEBHOOK=${FEISHU_WEBHOOK:-}

if [ -z "$BAIDU_APPID" ] || [ -z "$BAIDU_SECRET" ]; then
    echo "错误：请设置环境变量 BAIDU_APPID 和 BAIDU_SECRET"
    exit 1
fi

retry() {
    local n=0 max=3 delay=2
    until [ $n -ge $max ]; do
        "$@" && return 0
        n=$((n+1))
        echo "命令失败，${delay}秒后重试 ($n/$max)..." >&2
        sleep $delay
    done
    echo "命令最终失败: $*" >&2
    return 1
}

translate() {
    local text="$1"
    local salt=$(date +%s)
    local sign=$(echo -n "$BAIDU_APPID$text$salt$BAIDU_SECRET" | md5sum | cut -d ' ' -f1)
    local encoded_text=$(echo -n "$text" | jq -sRr @uri)
    local result=$(retry curl -s --connect-timeout 10 --max-time 30 "https://fanyi-api.baidu.com/api/trans/vip/translate?q=$encoded_text&from=auto&to=zh&appid=$BAIDU_APPID&salt=$salt&sign=$sign")
    echo "$result" | jq -r '.trans_result[0].dst // ""'
}

fetch_rss() {
    local url="$1"
    local tmp=$(mktemp)
    retry curl -s --connect-timeout 10 --max-time 30 -A "Mozilla/5.0" "$url" > "$tmp"
    if command -v xmlstarlet >/dev/null 2>&1; then
        xmlstarlet sel -t -m "//item" -v "title" -o "||" -v "link" -o "||" -n "$tmp" 2>/dev/null
    else
        echo "错误：未安装 xmlstarlet，请运行 sudo apt install xmlstarlet -y" >&2
        return 1
    fi
    rm "$tmp"
}

fetch_hackernews() {
    local tmp=$(mktemp)
    retry curl -s https://hacker-news.firebaseio.com/v0/topstories.json | jq -r '.[0:20][]' > "$tmp"
    while read id; do
        local item=$(retry curl -s "https://hacker-news.firebaseio.com/v0/item/$id.json")
        local title=$(echo "$item" | jq -r '.title')
        local url=$(echo "$item" | jq -r '.url')
        [ "$url" = "null" ] && url="https://news.ycombinator.com/item?id=$id"
        echo "$title||$url"
    done < "$tmp"
    rm "$tmp"
}

match_keywords() {
    local title="$1"
    [ -z "$KEYWORDS" ] && return 0
    IFS=',' read -ra kw <<< "$KEYWORDS"
    for k in "${kw[@]}"; do
        echo "$title" | grep -iq "${k// /}" && return 0
    done
    return 1
}

notify_error() {
    local error_msg="$1"
    if [ -n "$FEISHU_WEBHOOK" ]; then
        local json=$(jq -n --arg msg "❌ 外贸资讯聚合器运行失败\n\n错误详情: $error_msg" '{"msg_type":"text","content":{"text":$msg}}')
        curl -X POST -H "Content-Type: application/json" -d "$json" "$FEISHU_WEBHOOK" > /dev/null 2>&1
    fi
}

OUTPUT="$HOME/trade-news.md"
DATE=$(date '+%Y-%m-%d')
declare -A seen
declare -a final_titles
declare -a final_urls
COUNT=0

ALL_NEWS=""
[ "$INCLUDE_HACKER_NEWS" = "true" ] && ALL_NEWS+=$'\n'"$(fetch_hackernews)"
if [ -n "$RSS_FEEDS" ]; then
    IFS=',' read -ra feeds <<< "$RSS_FEEDS"
    for feed in "${feeds[@]}"; do
        feed=$(echo "$feed" | tr -d ' ')
        ALL_NEWS+=$'\n'"$(fetch_rss "$feed")"
    done
fi

while IFS='||' read -r title url; do
    [ -z "$title" ] && continue
    title=$(echo "$title" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    url=$(echo "$url" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    [ -n "${seen["$title"]}" ] && continue
    seen["$title"]=1
    if match_keywords "$title"; then
        final_titles[$COUNT]="$title"
        final_urls[$COUNT]="$url"
        COUNT=$((COUNT+1))
        [ $COUNT -ge $MAX_ITEMS ] && break
    fi
done <<< "$ALL_NEWS"

{
    echo "# 每日外贸资讯汇总 - $DATE"
    echo ""
    echo "## 相关资讯（关键词: ${KEYWORDS:-无}）"
    echo ""
    for ((i=0; i<COUNT; i++)); do
    title="${final_titles[$i]}"
    url="${final_urls[$i]}"
    num=$((i+1))
    zh=$(translate "$title")
    # 清理链接
    clean_url=$(echo "$url" | sed 's/^[| ]*//;s/[| ]*$//;s/&amp;/\&/g')
    # 标题变成可点击链接
    echo "**$num. [$title]($clean_url)**"
    [ -n "$zh" ] && [ "$zh" != "null" ] && echo "   - 中文: $zh"
    echo ""
    sleep 1
done
    echo "✅ 共抓取 $COUNT 条新闻"
} > "$OUTPUT"

if [ $COUNT -eq 0 ]; then
    notify_error "未抓取到任何新闻，请检查网络连接、代理或 RSS 源配置。"
    exit 1
fi

if [ -n "$FEISHU_WEBHOOK" ]; then
    CARD_JSON=$(jq -n \
        --arg title "📰 每日外贸资讯 - $DATE" \
        --arg content "$(cat "$OUTPUT")" \
        '{
            "msg_type": "interactive",
            "card": {
                "config": {"wide_screen_mode": true},
                "header": {"title": {"tag": "plain_text", "content": $title}, "template": "blue"},
                "elements": [
                    {"tag": "div", "text": {"tag": "lark_md", "content": $content}},
                    {"tag": "hr"},
                    {"tag": "note", "elements": [{"tag": "plain_text", "content": "Generated by OpenClaw | 外贸资讯聚合器 v2.2.3"}]}
                ]
            }
        }')
    curl -X POST -H "Content-Type: application/json" -d "$CARD_JSON" "$FEISHU_WEBHOOK" > /dev/null 2>&1
    echo "✅ 已推送到飞书（卡片消息）"
fi

# 调用分类推送脚本
python3 "$(dirname "$0")/classify_news.py"

# 趋势分析（每日保存数据，积累7天后自动推送周报）
python3 "$(dirname "$0")/trend_analysis.py"

echo "资讯汇总已完成！文件位置：$OUTPUT"
