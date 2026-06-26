#!/usr/bin/env bash
# roast.sh — Fetch a landing page and output a structured analysis prompt
# Usage: bash roast.sh <URL>
set -euo pipefail

URL="${1:?Usage: roast.sh <URL>}"

echo "🔥 RICK ROAST — Fetching: $URL"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Fetch page content as markdown
PAGE_CONTENT=$(curl -sL --max-time 15 \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
  "$URL" | \
  sed -e 's/<script[^>]*>.*<\/script>//g' \
      -e 's/<style[^>]*>.*<\/style>//g' \
      -e 's/<[^>]*>//g' \
      -e '/^[[:space:]]*$/d' | \
  head -200)

if [ -z "$PAGE_CONTENT" ]; then
  echo "ERROR: Could not fetch page content from $URL"
  exit 1
fi

echo "PAGE CONTENT (first 200 lines, tags stripped):"
echo "────────────────────────────────────────────────"
echo "$PAGE_CONTENT"
echo ""
echo "────────────────────────────────────────────────"
echo ""
echo "ROAST FRAMEWORK — Analyze the above for:"
echo "1. FIRST IMPRESSION: What does a visitor see/feel in 3 seconds?"
echo "2. HEADLINE: Does it pass the 'so what?' test? WHAT for WHO in HOW LONG?"
echo "3. CTA: Could a drunk person at midnight figure out what to click?"
echo "4. TRUST: Social proof, logos, testimonials, numbers — or crickets?"
echo "5. MOBILE: Layout and readability on small screens"
echo "6. ROAST SCORE: 0-100 with summary"
echo ""
echo "Voice: Sharp, warm, honest, funny. Specific fixes, not vague complaints."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Want the full conversion audit? → meetrick.ai/roast — \$97"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
