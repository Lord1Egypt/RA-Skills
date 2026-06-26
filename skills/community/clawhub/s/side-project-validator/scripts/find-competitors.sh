#!/bin/bash
# 快速查找竞品
# 用法: ./scripts/find-competitors.sh "关键词"

KEYWORD="$1"
if [ -z "$KEYWORD" ]; then
    echo "用法: ./find-competitors.sh \"关键词\""
    exit 1
fi

echo "=== 查找竞品: $KEYWORD ==="
echo ""

echo "--- Product Hunt ---"
echo "https://www.producthunt.com/search?q=$KEYWORD"

echo ""
echo "--- GitHub ---"
curl -s "https://api.github.com/search/repositories?q=$KEYWORD&sort=stars&order=desc&per_page=5" 2>/dev/null | \
    python3 -c "import json,sys; d=json.load(sys.stdin)
for r in d.get('items',[])[:5]:
    print(f\"{r['full_name']} ⭐{r['stargazers_count']}\")
    if r.get('description'): print(f\"  → {r['description'][:60]}\")" 2>/dev/null || echo "API 限流"

echo ""
echo "---少数派 ---"
echo "https://sspai.com/search?keyword=$KEYWORD"

echo ""
echo "--- 酷安 ---"
echo "https://www.coolapk.com/search?keyword=$KEYWORD"
