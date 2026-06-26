#!/bin/bash

# Auto AI tweet generator (non-interactive)
POST_SCRIPT="/Users/youke/.openclaw/workspace/skills/zeelin-twitter-web-autopost/scripts/tweet.sh"

# Fetch latest AI related headlines from Hacker News API
HEADLINES=$(python3 - << 'PY'
import requests
try:
    r = requests.get("https://hn.algolia.com/api/v1/search?query=AI&tags=story&hitsPerPage=5")
    data = r.json()
    titles = [h['title'] for h in data.get('hits', []) if h.get('title')][:3]

    # Ensure English‑only output (remove non‑ASCII characters)
    clean = []
    for t in titles:
        t = t.encode("ascii", "ignore").decode()
        clean.append(t)
    formatted = "\n".join([f"• {t}" for t in clean])
    print(formatted)
except Exception:
    print("• New developments in AI agents\n• Open‑source AI momentum growing\n• Reasoning models improving")
PY
)

# Choose tweet style: 0=news,1=insight,2=builder
TYPE=$((RANDOM % 3))

REPORT_URL="https://thu-nmrc.github.io/THU-ZeeLin-Reports/"

if [ "$TYPE" -eq 0 ]; then
TWEET="New AI research report released.

${HEADLINES}

Report:
${REPORT_URL}

#AI #TechTwitter"
elif [ "$TYPE" -eq 1 ]; then
TWEET="Latest AI research highlights.

${HEADLINES}

Report:
${REPORT_URL}

#AI #TechTwitter"
else
TWEET="New insights from recent AI research.

${HEADLINES}

Report:
${REPORT_URL}

#AI #TechTwitter"
fi

# Enforce Twitter 280 char limit (target <=260 to leave margin)
MAX=260
LEN=${#TWEET}
if [ "$LEN" -gt "$MAX" ]; then
  TWEET="${TWEET:0:$MAX}…"
fi

bash "$POST_SCRIPT" "$TWEET" "https://x.com"