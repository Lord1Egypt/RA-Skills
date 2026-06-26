#!/bin/bash
# Research a keyword: check volume, analyze competition, get suggestions
# Usage: ./research-keyword.sh "keyword" [lang] [location]
# lang: en (default) or fr
# location: 2840 (US, default) or 2250 (France)

KEYWORD="$1"
LANG="${2:-en}"
LOCATION="${3:-2840}"

if [ -z "$KEYWORD" ]; then
  echo "Usage: $0 \"keyword\" [lang] [location]"
  echo "  lang: en (default), fr"
  echo "  location: 2840 (US), 2250 (France)"
  exit 1
fi

DFORSEO_LOGIN="${DATAFORSEO_LOGIN}"
DFORSEO_PASS="${DATAFORSEO_PASSWORD}"

if [ -z "$DFORSEO_LOGIN" ] || [ -z "$DFORSEO_PASS" ]; then
  echo "Error: DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD env vars are required."
  echo "Get your credentials at https://dataforseo.com"
  exit 1
fi

echo "=== Keyword Research: $KEYWORD (lang=$LANG, loc=$LOCATION) ==="
echo ""

# 1. Search volume
echo "--- Search Volume ---"
curl -s -X POST "https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live" \
  -u "$DFORSEO_LOGIN:$DFORSEO_PASS" \
  -H "Content-Type: application/json" \
  -d "[{\"keywords\":[\"$KEYWORD\"],\"language_code\":\"$LANG\",\"location_code\":$LOCATION}]" | \
  python3 -c "
import sys,json
d=json.load(sys.stdin)
for r in d['tasks'][0]['result']:
    sv = r.get('search_volume') or 0
    cpc = r.get('cpc') or 0
    comp = r.get('competition') or 'N/A'
    ms = r.get('monthly_searches') or []
    trend = [m.get('search_volume',0) for m in ms[:6]] if ms else []
    print(f'Volume: {sv}/month  CPC: \${cpc}  Competition: {comp}')
    print(f'Trend (recent 6mo): {trend}')
"

echo ""

# 2. Related keywords
echo "--- Related Keywords (top 15 by volume) ---"
curl -s -X POST "https://api.dataforseo.com/v3/keywords_data/google_ads/keywords_for_keywords/live" \
  -u "$DFORSEO_LOGIN:$DFORSEO_PASS" \
  -H "Content-Type: application/json" \
  -d "[{\"keywords\":[\"$KEYWORD\"],\"language_code\":\"$LANG\",\"location_code\":$LOCATION,\"sort_by\":\"search_volume\",\"limit\":15}]" | \
  python3 -c "
import sys,json
d=json.load(sys.stdin)
for r in d['tasks'][0]['result'][:15]:
    sv = r.get('search_volume') or 0
    cpc = r.get('cpc') or 0
    comp = r.get('competition') or 'N/A'
    kw = r.get('keyword','')
    print(f'{kw:50} vol:{sv:>6}  cpc:\${cpc:>8}  comp:{comp}')
"

echo ""

# 3. Google Suggest
echo "--- Google Suggest ---"
curl -s -A "Mozilla/5.0" "https://suggestqueries.google.com/complete/search?client=firefox&q=$(echo $KEYWORD | sed 's/ /+/g')" 2>/dev/null | \
  python3 -c "import sys,json; [print(x) for x in json.load(sys.stdin)[1]]" 2>/dev/null

echo ""
echo "=== Done ==="
