#!/bin/bash
# 调研市场需求强度
# 用法: ./scripts/research-demand.sh "关键词"

KEYWORD="$1"
if [ -z "$KEYWORD" ]; then
    echo "用法: ./research-demand.sh \"关键词\""
    exit 1
fi

echo "=== 需求调研: $KEYWORD ==="
echo ""

echo "--- 知乎相关问题 ---"
curl -s "https://www.zhihu.com/api/v4/search_v5?q=$KEYWORD&type=topic" 2>/dev/null | \
    python3 -c "import json,sys; d=json.load(sys.stdin)
for item in d.get('data',[])[:3]:
    if item.get('question'): print(f\"Q: {item['question']['title']}\")" 2>/dev/null || echo "知乎查询失败，手动查看: https://www.zhihu.com/search?q=$KEYWORD"

echo ""
echo "--- Reddit 相关讨论 ---"
echo "https://www.reddit.com/search/?q=$KEYWORD"

echo ""
echo "--- B站相关视频 ---"
echo "https://search.bilibili.com/all?keyword=$KEYWORD&order=pubdate"

echo ""
echo "--- 小红书笔记 ---"
echo "https://www.xiaohongshu.com/search_result?keyword=$KEYWORD"
