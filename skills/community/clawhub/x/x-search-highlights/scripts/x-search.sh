#!/bin/bash
# x-search-highlights.sh
# Search X/Twitter for high-engagement posts

set -e

# Parameters
TOPIC="${1:-Claude Code}"
MAX_RESULTS="${2:-5}"
SCROLL_TIMES="${3:-3}"
MIN_LIKES="${4:-0}"
OUTPUT_FORMAT="${5:-markdown}"

# Encode topic for URL
TOPIC_ENCODED=$(echo "$TOPIC" | sed 's/ /+/g')

echo "🔍 Searching X for: $TOPIC"
echo "   Max results: $MAX_RESULTS | Min likes: $MIN_LIKES | Scrolls: $SCROLL_TIMES"

# 1. Open search page
echo "📱 Opening search page..."
bb-browser open "https://x.com/search?q=${TOPIC_ENCODED}&src=typed_query&f=top" --json 2>&1 | head -1
sleep 3

# 2. Scroll to load more content
echo "⏳ Loading content ($SCROLL_TIMES scrolls)..."
for i in $(seq 1 $SCROLL_TIMES); do
  bb-browser eval 'window.scrollTo(0, document.body.scrollHeight); "scroll_'$i'";' --json 2>&1 | tail -1
  sleep 2
done

# 3. Extract posts
echo "📊 Extracting posts..."
RESULT=$(bb-browser eval '
(function() {
  const maxResults = '"$MAX_RESULTS"';
  const minLikes = '"$MIN_LIKES"';
  
  const posts = document.querySelectorAll("article");
  const results = [];
  
  const getNum = (el) => {
    if (!el) return 0;
    const aria = el.getAttribute("aria-label") || "";
    const m = aria.match(/(\d+\.?\d*[KM]?)/i);
    if (!m) return 0;
    let n = m[1].toUpperCase();
    if (n.includes("K")) return parseFloat(n) * 1000;
    if (n.includes("M")) return parseFloat(n) * 1000000;
    return parseInt(n);
  };
  
  posts.forEach(p => {
    try {
      const txt = p.querySelector("[data-testid=\"tweetText\"]");
      const tm = p.querySelector("time");
      const au = p.querySelector("[data-testid=\"User-Name\"]");
      
      if (!txt) return;
      
      const likes = getNum(p.querySelector("button[aria-label*=\"Like\"]"));
      if (likes < minLikes) return;
      
      const text = txt.innerText.trim();
      const author = au ? au.innerText.split("\n")[0] : "";
      const handle = au ? (au.innerText.match(/@[\w]+/)?.[0] || "") : "";
      const date = tm ? (tm.getAttribute("datetime") || tm.innerText) : "";
      const url = tm ? tm.closest("a")?.href : "";
      
      results.push({
        text: text.slice(0, 250),
        fullText: text,
        author: author,
        handle: handle,
        date: date,
        url: url,
        replies: getNum(p.querySelector("button[aria-label*=\"Repl\"]")),
        retweets: getNum(p.querySelector("button[aria-label*=\" repost\"]")),
        likes: likes,
        views: getNum(p.querySelector("a[href*=\"/analytics\"]"))
      });
    } catch(e) {}
  });
  
  // Sort by engagement score
  results.sort((a,b) => {
    const sA = (a.likes||0)*2 + (a.retweets||0)*5 + (a.views||0)*0.01;
    const sB = (b.likes||0)*2 + (b.retweets||0)*5 + (b.views||0)*0.01;
    return sB - sA;
  });
  
  return JSON.stringify({
    topic: "'"$TOPIC"'",
    totalFound: results.length,
    returned: Math.min(maxResults, results.length),
    posts: results.slice(0, maxResults)
  }, null, 2);
})();
' --json 2>&1)

# 4. Parse and format output
if [ "$OUTPUT_FORMAT" == "json" ]; then
  echo "$RESULT" | jq -r '.result' 2>/dev/null || echo "$RESULT"
else
  # Markdown format
  echo ""
  echo "---"
  echo "## 🔍 $TOPIC - 搜索结果"
  echo ""
  
  # Parse JSON and format
  echo "$RESULT" | jq -r '.result' 2>/dev/null | jq -r '.posts[]' 2>/dev/null | \
  while IFS= read -r line; do
    # Extract fields from JSON (simple parsing)
    if [[ "$line" =~ '"author"' ]]; then
      AUTHOR=$(echo "$line" | jq -r '.author' 2>/dev/null)
      HANDLE=$(echo "$line" | jq -r '.handle' 2>/dev/null)
      TEXT=$(echo "$line" | jq -r '.text' 2>/dev/null)
      DATE=$(echo "$line" | jq -r '.date' 2>/dev/null | cut -d'T' -f1)
      URL=$(echo "$line" | jq -r '.url' 2>/dev/null)
      LIKES=$(echo "$line" | jq -r '.likes' 2>/dev/null)
      RETWEETS=$(echo "$line" | jq -r '.retweets' 2>/dev/null)
      REPLIES=$(echo "$line" | jq -r '.replies' 2>/dev/null)
      VIEWS=$(echo "$line" | jq -r '.views' 2>/dev/null)
      
      echo ""
      echo "### $AUTHOR ($HANDLE)"
      echo "- **日期**：$DATE"
      echo "- **内容摘要**：$TEXT"
      echo "- **互动**：$REPLIES 回复 · $RETWEETS 转发 · $LIKES 点赞 · $VIEWS 浏览"
      echo "- **链接**：[点击阅读原文]($URL)"
      echo ""
    fi
  done
fi

echo "---"
echo "✅ 完成：找到 $(echo "$RESULT" | jq -r '.result.totalFound' 2>/dev/null) 条帖子，返回前 $MAX_RESULTS 条"