# X API Quick Reference

## Setup (30 seconds)

```bash
# 1. Create credentials file
mkdir -p ~/.openclaw/x
cat > ~/.openclaw/x/credentials.json <<EOF
{
  "bearer_token": "YOUR_BEARER_TOKEN_HERE"
}
EOF

# 2. Get your bearer token:
# https://developer.x.com/en/portal/projects-and-apps
# → Your app → Keys and tokens → Bearer Token

# 3. Test
python3 scripts/x.py user steipete
```

## Most Common Commands

```bash
# User info
x.py user <username>

# Recent tweets
x.py timeline <username> --max 50

# Search
x.py search "query" --max 20

# Thread
x.py thread <tweet_url>

# Single tweet
x.py tweet <id>
```

## One-Liners

```bash
# Get someone's latest non-retweet
x.py timeline steipete --max 1 --exclude retweets

# Search from specific user
x.py search "from:steipete OpenClaw" --max 10

# Batch lookup 3 tweets
x.py tweets 123 456 789

# Get user bio
x.py user steipete | grep Bio
```

## OAuth (for Bookmarks/Posting)

```bash
# One-time setup
x.py auth

# Then use
x.py bookmarks --max 100
x.py likes steipete --max 50
x.py post "Hello world!"
```

## Output Formats

Clean, grep-friendly text:

```
👤 Name (@username)
   ID: 12345
   Bio: ...
   👥 followers · following · tweets

🐦 Tweet text
   📅 timestamp
   ❤️ likes 🔁 retweets 💬 replies
   https://x.com/...
```

## Rate Limits (per 15 min)

- Timeline: ~1,500 requests
- Search: 450 requests
- User lookup: 900 requests
- Tweet lookup: 900 requests

**Tip:** Add `sleep 1` between requests in loops.

## Search Operators

```bash
# From user
x.py search "from:steipete OpenAI"

# Exclude retweets
x.py search "OpenClaw -filter:retweets"

# Date range
x.py search "OpenClaw since:2026-02-01 until:2026-02-20"

# Verified only
x.py search "OpenClaw filter:verified"
```

## Pipe to jq (if needed)

The tool outputs text, not JSON. For structured data:

```bash
# Use the API directly
curl "https://api.x.com/2/users/by/username/steipete" \
  -H "Authorization: Bearer $TOKEN" | jq .
```

Or modify the script to add `--json` flag if needed.
