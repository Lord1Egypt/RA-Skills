#!/usr/bin/env bash
# Fallback search script - tries tools in priority order T1→T7
# Usage: ./fallback-search.sh "query" [count]
# No API keys in this script - reads from .env files in respective skill directories

set -uo pipefail

QUERY="${1:?Usage: $0 <query> [count]}"
COUNT="${2:-5}"

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
WORKSPACE="$(dirname "$SKILL_DIR")"

echo "🔍 Searching: $QUERY"
echo "---"

# T1: web-search-plus (Serper)
echo "Trying T1: web-search-plus (Serper)..."
if python3 "$WORKSPACE/web-search-plus/scripts/search.py" -q "$QUERY" --count "$COUNT" 2>/dev/null; then
    echo "✅ T1 succeeded"
    exit 0
fi
echo "❌ T1 failed, trying T2..."

# T2: opencli google search (免 Key)
echo "Trying T2: opencli google search..."
if opencli google search "$QUERY" --limit "$COUNT" -f json 2>/dev/null; then
    echo "✅ T2 succeeded"
    exit 0
fi
echo "❌ T2 failed, trying T3..."

# T3: multi-search-engine (via crawl4ai - 爬百度)
echo "Trying T3: crawl4ai → 百度..."
if python3 -c "
import asyncio
from crawl4ai import AsyncWebCrawler
async def main():
    async with AsyncWebCrawler() as c:
        r = await c.arun(url='https://www.baidu.com/s?wd=$QUERY')
        print(r.markdown[:3000])
asyncio.run(main())
" 2>/dev/null; then
    echo "✅ T3 succeeded"
    exit 0
fi
echo "❌ T3 failed, trying T4..."

# T4: crawl4ai (needs specific URL)
echo "T4: crawl4ai - needs specific URL, skipping automated fallback"

# T5: firecrawl-cli
echo "Trying T5: firecrawl-cli..."
if firecrawl search "$QUERY" --limit "$COUNT" 2>/dev/null; then
    echo "✅ T5 succeeded"
    exit 0
fi
echo "❌ T5 failed"

echo ""
echo "⚠️  All automated search tools failed. Try:"
echo "  1. Provide a specific URL for web_fetch or crawl4ai"
echo "  2. OpenCLI vertical search (zhihu, bilibili, etc.)"
echo "  3. Manual search in browser"
exit 1
