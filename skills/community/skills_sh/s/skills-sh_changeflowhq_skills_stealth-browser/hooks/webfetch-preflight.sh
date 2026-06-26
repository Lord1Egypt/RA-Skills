#!/bin/bash
# PreToolUse hook for WebFetch - skip known-blocked domains
#
# Checks the URL's domain against a learned blocklist.
# If the domain has been blocked before, blocks the WebFetch call
# and tells Claude to use stealth-browser instead.

BLOCKLIST="$HOME/.claude/skills/stealth-browser/data/blocked-domains.txt"

# No blocklist file = nothing to check
if [ ! -f "$BLOCKLIST" ]; then
  exit 0
fi

input=$(cat)

# Extract URL from the hook input JSON
url=$(echo "$input" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('url',''))" 2>/dev/null)

if [ -z "$url" ]; then
  exit 0
fi

# Extract domain from URL
domain=$(echo "$url" | python3 -c "import sys; from urllib.parse import urlparse; print(urlparse(sys.stdin.read().strip()).netloc)" 2>/dev/null)

if [ -z "$domain" ]; then
  exit 0
fi

# Check if domain (or parent domain) is in blocklist
if grep -qiF "$domain" "$BLOCKLIST" 2>/dev/null; then
  echo "DOMAIN PREVIOUSLY BLOCKED ($domain) - Skip WebFetch. Use stealth-browser directly:"
  echo "  ~/.claude/skills/stealth-browser/scripts/stealth-browser read $url"
  echo ""
  echo "To remove from blocklist: edit ~/.claude/skills/stealth-browser/data/blocked-domains.txt"
  exit 2
fi

exit 0
