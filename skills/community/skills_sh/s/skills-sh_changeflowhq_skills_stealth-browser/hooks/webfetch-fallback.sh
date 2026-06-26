#!/bin/bash
# PostToolUse hook for WebFetch - catch soft blocks and learn blocked domains
#
# NOTE: Only fires on successful WebFetch calls (HTTP 200).
# Hard failures (403, 429, timeouts) throw errors and skip PostToolUse.
# Those are handled by the CLAUDE.md rule instead.

BLOCKLIST="$HOME/.claude/skills/stealth-browser/data/blocked-domains.txt"

input=$(cat)

response=$(echo "$input" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_response',{}).get('result',''))" 2>/dev/null)
url=$(echo "$input" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('url',''))" 2>/dev/null)

if echo "$response" | grep -qiE 'cloudflare|just.a.moment|challenge-platform|captcha|bot.protection|verify.you.are.human|checking.your.browser|ray.id'; then
  # Learn: add domain to blocklist so future calls skip WebFetch entirely
  domain=$(echo "$url" | python3 -c "import sys; from urllib.parse import urlparse; print(urlparse(sys.stdin.read().strip()).netloc)" 2>/dev/null)
  if [ -n "$domain" ]; then
    mkdir -p "$(dirname "$BLOCKLIST")"
    if ! grep -qxF "$domain" "$BLOCKLIST" 2>/dev/null; then
      echo "$domain" >> "$BLOCKLIST"
    fi
  fi

  echo "WEBFETCH GOT A CHALLENGE PAGE - Domain '$domain' added to blocklist. Retry with stealth-browser:"
  echo "  ~/.claude/skills/stealth-browser/scripts/stealth-browser read $url"
fi

exit 0
