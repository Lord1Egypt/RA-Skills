---
name: reddit-publisher
description: Research subreddits, draft Reddit-native posts, and publish/schedule via Late API. Includes ScrapeCreators for reading (search, subreddit details, comments) and Late for writing (validate, flairs, post). Built-in anti-AI-slop pass ensures posts sound human.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - SCRAPECREATORS_API_KEY
        - LATE_API_KEY
      bins:
        - python3
      config:
        - ~/.config/scrapecreators/api_key
        - ~/.config/late/api_key
    primaryEnv: LATE_API_KEY
    emoji: "🟠"
    homepage: https://clawhub.ai/skills/reddit-publisher
---

# Reddit Publisher

Research, draft, and publish Reddit posts that sound human.

## Setup

### ScrapeCreators (reading Reddit)
1. Get an API key at [scrapecreators.com](https://scrapecreators.com)
2. Save it: `mkdir -p ~/.config/scrapecreators && echo "YOUR_KEY" > ~/.config/scrapecreators/api_key && chmod 600 ~/.config/scrapecreators/api_key`

### Late (posting to Reddit)
1. Get an API key at [getlate.dev](https://getlate.dev)
2. Connect your Reddit account in the Late dashboard
3. Save the key: `mkdir -p ~/.config/late && echo "YOUR_KEY" > ~/.config/late/api_key && chmod 600 ~/.config/late/api_key`
4. Find your Reddit account ID: `python3 ./scripts/late_reddit.py accounts`

## Tooling

### ScrapeCreators (READ Reddit)
```bash
# Search Reddit globally
python3 ./scripts/sc_reddit.py search --query "AI agent" --timeframe week

# Search within a subreddit
python3 ./scripts/sc_reddit.py subreddit-search --subreddit nocode --query "automation" --timeframe month

# Get subreddit details (size, description)
python3 ./scripts/sc_reddit.py subreddit-details --subreddit microsaas

# Get post + comments
python3 ./scripts/sc_reddit.py post-comments --url "https://www.reddit.com/r/.../comments/..."

# Search Reddit Ad Library
python3 ./scripts/sc_reddit.py ads-search --query "Notion"
```

### Late (WRITE to Reddit)
```bash
# List connected Reddit accounts
python3 ./scripts/late_reddit.py accounts

# Validate subreddit exists
python3 ./scripts/late_reddit.py validate-subreddit --subreddit r/microsaas

# List available flairs
python3 ./scripts/late_reddit.py reddit-flairs --account-id <ACCOUNT_ID> --subreddit microsaas

# Post now
python3 ./scripts/late_reddit.py create-post --account-id <ACCOUNT_ID> --subreddit microsaas --title "My title" --body "My body"

# Schedule a post
python3 ./scripts/late_reddit.py create-post --account-id <ACCOUNT_ID> --subreddit microsaas --title "My title" --body "My body" --scheduled-for 2026-04-01T10:00:00Z
```

## Writing workflow

When drafting a Reddit post or comment:

### 1. Write Reddit-native
- Open with the concrete situation in 1-2 lines (what you did, what happened)
- Give specific details (numbers, stack, time spent, what you tried)
- End with a real question or request for feedback

### 2. Anti-AI-slop pass (mandatory)
Read the references before finalizing any draft:
- `./references/stop-slop/phrases.md` — words and phrases to remove
- `./references/stop-slop/structures.md` — patterns to avoid
- `./references/stop-slop/examples.md` — before/after calibration

### 3. Quick checklist
- No throat-clearing openers ("Here's the thing", "Let me be clear")
- No binary contrast frames ("Not X. Y.")
- Active voice, name the actor
- Cut adverbs and vague importance claims
- No em dashes. Use commas or periods
- No "I'd be happy to" or "Great question"

## Pre-flight before posting
1. Check subreddit details (ScrapeCreators) for rules and size
2. List flairs (Late) and pick one if required
3. Keep first post in any sub low-risk (text post, no links in first paragraph)
4. Many subreddits require flair — posts without flair get auto-removed
5. New/low-karma accounts get blocked on many subs

## Post tracking (optional)
Create a file `references/post-history.md` to track your posts:
- Sub, title, date, score, upvote ratio, comments, status
- Review what works vs what gets buried
- Don't repeat the same angle in the same sub within 2 weeks

## Things to know
- ScrapeCreators is read-only (1 credit per request)
- Late: no video uploads, no analytics for Reddit
- Reddit rules differ by subreddit — always check before posting
- No API can guarantee posting success in every subreddit
