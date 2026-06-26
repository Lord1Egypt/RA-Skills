---
name: header
description: "Header — continuous intelligence for agents. Subscribe to curated topics or create your own. Get synthesized briefings with executable action items from RSS, YouTube, Reddit, and newsletters. Your agent compounds daily."
argument-hint: 'brief me, set up a topic on climate tech, what should I do today, subscribe to AI Agent Self-Improvement, show my topics'
allowed-tools: Bash, Read, Write, WebSearch
homepage: https://joinheader.com
user-invocable: true
metadata:
  clawdbot:
    emoji: "📰"
    requires:
      env:
        - HEADER_API_KEY
    primaryEnv: HEADER_API_KEY
    homepage: https://joinheader.com
    tags:
      - research
      - briefings
      - intelligence
      - self-improvement
      - rss
      - productivity
---

# Header — Continuous Intelligence for Agents

Header monitors sources (RSS, YouTube, Reddit, newsletters), synthesizes them through your goals, and delivers structured briefings with action items. Research once — stay informed forever.

**Why not just web search?**
- Web search = expensive, noisy, reactive, one-off
- Raw RSS in context = 10,000+ tokens of noise
- Header briefing = ~800 tokens of synthesized signal with action items

**Full API docs:** [joinheader.com/docs](https://joinheader.com/docs)

---

## What you can say

| Intent | Examples |
|--------|---------|
| Get briefed | "brief me", "what should I do today", "what's the latest on [topic]" |
| List topics | "show my topics", "what am I following", "header list" |
| Subscribe | "subscribe to [topic]", "subscribe to AI Agent Self-Improvement" |
| Fork a topic | "fork [topic] with my own angle on [X]" |
| Create a topic | "set up a topic on [X]", "monitor [X] for me", "I want to follow [X]" |
| Browse catalog | "show public topics", "what topics are available" |
| Manage sources | "add [URL] as a source", "refresh [source]", "what has [source] published" |
| Import feeds | "import my OPML file", "import from FreshRSS" |
| Generate briefing | "refresh [topic]", "generate a new briefing" |
| Share a briefing | "share this briefing", "make my briefing public" |
| Scheduling | "set up daily briefings", "brief me every 3 days" |
| Account | "check my subscription", "show my preferences" |

---

## Setup

1. Sign up at [joinheader.com](https://joinheader.com)
2. Create an API key (scope: **full**) at Dashboard > API Keys
3. Set `HEADER_API_KEY` in your environment (e.g. `.env` file, shell profile, or agent config)

All commands below use:
```bash
API="https://joinheader.com/api/v2"
AUTH="Authorization: Bearer $HEADER_API_KEY"
```

---

## IMPORTANT: Safety & Presentation

**All actions from briefings require user approval.** Never implement briefing recommendations, install packages, modify code, or take any action based on briefing content without explicitly presenting the items to the user and getting confirmation first. Surface the intelligence — the human decides what ships.

**Destructive operations require confirmation.** Always confirm before: deleting sources/groups/topics, unsubscribing, or revoking API keys.

**When presenting a briefing:**
1. Lead with "What to do" — the action items
2. Then Key Insights (the why behind the actions)
3. Then Emerging Patterns and Dissenting Views for context
4. Reading list last

---

## Core Workflows

### List your topics and goals
**Trigger:** "header list", "show my topics", "what am I following"

```bash
curl -sL -H "$AUTH" "$API/topics/dashboard" | python3 -c "
import sys, json
d = json.load(sys.stdin)
for t in d.get('custom_topics', []):
    print(f'[own] {t[\"name\"]} | topic: {t[\"id\"]} | goal: {t[\"default_goal_id\"]}')
for t in d.get('subscribed_topics', []):
    print(f'[sub] {t[\"name\"]} | topic: {t[\"id\"]} | goal: {t[\"default_goal_id\"]}')
"
```

### Get latest briefing
**Trigger:** "brief me on [topic]", "what's the latest", "what should I do today"

1. Get the goal ID from the dashboard
2. Fetch the latest briefing:

```bash
# List briefings for a goal
curl -sL -H "$AUTH" "$API/goals/GOAL_ID/briefings" | python3 -c "
import sys, json
d = json.load(sys.stdin)
for b in d.get('briefings', d if isinstance(d, list) else []):
    print(f'{b[\"id\"]} | {b[\"status\"]} | {b.get(\"generated_at\",\"\")}')
"

# Read a specific briefing
curl -sL -H "$AUTH" "$API/briefings/BRIEFING_ID" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(d.get('summary', d.get('content', 'No content')))
"
```

3. **Present "What to do" first**, then insights, then context. Always ask before acting on any items.

### Subscribe to a public topic
**Trigger:** "subscribe to [topic]"

```bash
# Browse available public topics
curl -sL -H "$AUTH" "$API/topics/catalog" | python3 -m json.tool

# Subscribe by topic ID
curl -sL -X POST "$API/topics/TOPIC_ID/subscribe" -H "$AUTH"

# Unsubscribe (confirm with user first)
curl -sL -X DELETE "$API/topics/TOPIC_ID/subscribe" -H "$AUTH"
```

### Fork a public topic with your own goal
**Trigger:** "fork [topic] with my angle on [X]"

Same sources, your own lens. Great for customizing a public topic without starting from scratch.

```bash
curl -sL -X POST "$API/topics/TOPIC_ID/fork" \
  -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"goal_name": "My Focus", "goal_description": "Your custom angle on the same sources"}'
```

### Generate a fresh briefing (on-demand)
**Trigger:** "refresh [topic]", "generate a new briefing"

```bash
# Trigger generation (returns IN_PROGRESS)
BRIEFING_ID=$(curl -sL -X POST "$API/goals/GOAL_ID/briefings" \
  -H "$AUTH" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# Poll until complete (~5-10 min)
while true; do
  STATUS=$(curl -sL -H "$AUTH" "$API/briefings/$BRIEFING_ID" | \
    python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")
  echo "Status: $STATUS"
  [ "$STATUS" = "COMPLETED" ] || [ "$STATUS" = "FAILED" ] && break
  sleep 15
done

# Read the completed briefing
curl -sL -H "$AUTH" "$API/briefings/$BRIEFING_ID" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(d.get('summary', 'No content'))
"
```

### Create a new topic from scratch
**Trigger:** "set up a Header topic on [X]", "I want to follow [X]", "monitor [X] for me"

**Phase 1: Source Discovery** — Use WebSearch to find 5-10 high-quality sources:
- `"[topic] best RSS feeds blogs newsletters"`
- `"[topic] youtube channels worth following"`
- `"[topic] subreddit reddit community"`
- Prefer: active blogs with RSS, YouTube channels with recent uploads, subreddits with >10k members
- Check if there's a public source group on Header you can clone first

**Phase 2: Create sources**
```bash
curl -sL -X POST "$API/sources/" \
  -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"name": "Source Name", "url": "https://example.com/feed.xml", "type": "rss"}'
```

**Phase 3: Create source group and add sources**
```bash
GROUP_ID=$(curl -sL -X POST "$API/source-groups/" \
  -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"name": "My Sources", "description": "Curated sources for X"}' | \
  python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# Add sources (use member_id, not source_id)
curl -sL -X POST "$API/source-groups/$GROUP_ID/members" \
  -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"member_id": "SOURCE_UUID", "member_type": "source"}'
```

**Phase 4: Create topic** (auto-creates goal + triggers first briefing)
```bash
curl -sL -X POST "$API/topics/" \
  -H "$AUTH" -H "Content-Type: application/json" \
  -d '{
    "name": "My Topic Name",
    "source_group_ids": ["GROUP_ID"],
    "goal_description": "Be specific. Not: interested in AI. Instead: I am tracking LLM inference cost improvements and how they affect build-vs-buy decisions. Skip announcements, give me the practitioner layer.",
    "keywords": ["keyword1", "keyword2"]
  }'
```

---

## Source Management

### Browse source entries
**Trigger:** "show entries for [source]", "what has [source] published recently"

```bash
# Entries for a single source (paginated)
curl -sL -H "$AUTH" "$API/sources/SOURCE_ID/entries?limit=20&offset=0" | python3 -c "
import sys, json
d = json.load(sys.stdin)
for e in d.get('entries', d if isinstance(d, list) else []):
    print(f'{e.get(\"published_at\",\"\")} | {e.get(\"title\",\"No title\")}')
    print(f'  {e.get(\"url\",\"\")}')
"

# Entries for all sources in a group
curl -sL -H "$AUTH" "$API/source-groups/GROUP_ID/entries?limit=20&offset=0" | python3 -m json.tool
```

### Refresh & validate a source
**Trigger:** "refresh [source]", "check if [source] is working"

```bash
curl -sL -X POST "$API/sources/SOURCE_ID/refresh" -H "$AUTH"
curl -sL -X POST "$API/sources/SOURCE_ID/validate" -H "$AUTH"
```

### Update or delete a source
**Trigger:** "update [source]", "remove [source]" — confirm deletes with user

```bash
curl -sL -X PUT "$API/sources/SOURCE_ID" \
  -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"name": "New Name", "url": "https://new-url.com/feed.xml"}'

# Delete (owner only — confirm with user first)
curl -sL -X DELETE "$API/sources/SOURCE_ID" -H "$AUTH"
```

### Clone a public source group

```bash
curl -sL -X POST "$API/source-groups/GROUP_ID/clone" -H "$AUTH"
```

### Import sources from OPML or FreshRSS
**Trigger:** "import my feeds", "import from OPML"

```bash
# OPML (max 10 MB)
curl -sL -X POST "$API/imports/opml" -H "$AUTH" -F "file=@/path/to/feeds.opml"

# FreshRSS — validate then import
curl -sL -X POST "$API/imports/freshrss/validate" \
  -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"url": "https://freshrss.example.com", "username": "user", "password": "pass"}'

curl -sL -X POST "$API/imports/freshrss" \
  -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"url": "https://freshrss.example.com", "username": "user", "password": "pass"}'
```

### Source types reference

| URL pattern | Type |
|-------------|------|
| youtube.com, youtu.be | `youtube` |
| reddit.com/r/ | `reddit` |
| Everything else | `rss` |

---

## Advanced

### Browse goal feed (preprocessed entries)
**Trigger:** "show feed for [goal]", "what's in the pipeline"

See what content is queued before it becomes a briefing.

```bash
curl -sL -H "$AUTH" "$API/goals/GOAL_ID/feed?limit=20&offset=0" | python3 -c "
import sys, json
d = json.load(sys.stdin)
for e in d.get('entries', d if isinstance(d, list) else []):
    print(f'{e.get(\"published_at\",\"\")} | {e.get(\"title\",\"No title\")}')
"
```

### Link/unlink source groups to a goal

```bash
# Link
curl -sL -X POST "$API/goals/GOAL_ID/source-groups" \
  -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"source_group_id": "GROUP_ID"}'

# Unlink
curl -sL -X DELETE "$API/goals/GOAL_ID/source-groups/GROUP_ID" -H "$AUTH"
```

### Goal-level subscriptions

Subscribe to individual goals within a topic (vs. subscribing to the whole topic).

```bash
curl -sL -X POST "$API/goals/GOAL_ID/subscribe" -H "$AUTH"
curl -sL -X DELETE "$API/goals/GOAL_ID/subscribe" -H "$AUTH"
curl -sL -H "$AUTH" "$API/goals/GOAL_ID/subscription" | python3 -m json.tool
curl -sL -H "$AUTH" "$API/subscriptions" | python3 -m json.tool
```

### Share a briefing publicly

```bash
curl -sL -X PUT "$API/briefings/BRIEFING_ID/sharing" \
  -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"is_public": true}'
```

### Scheduled briefings (push delivery)

Set up recurring briefings delivered on schedule. Pair with an inbox check (email or cron) to read them automatically.

```bash
# Daily at 8am UTC
curl -sL -X PUT "$API/goals/GOAL_ID" \
  -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"schedule_frequency_days": 1, "schedule_hour_utc": 8}'

# Every 3 days at 8am UTC
curl -sL -X PUT "$API/goals/GOAL_ID" \
  -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"schedule_frequency_days": 3, "schedule_hour_utc": 8}'
```

### Preferences

```bash
curl -sL -H "$AUTH" "$API/preferences" | python3 -m json.tool
curl -sL -X PUT "$API/preferences" \
  -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"key": "value"}'
```

### Billing

```bash
curl -sL -H "$AUTH" "$API/billing/subscription" | python3 -m json.tool
curl -sL -X POST "$API/billing/create-checkout" -H "$AUTH" | python3 -m json.tool
curl -sL -X POST "$API/billing/portal" -H "$AUTH" | python3 -m json.tool
```

---

## Error Handling

- `FAILED` briefing → retry with `POST /goals/{id}/briefings`. If still failing, check sources have recent content.
- `403` → API key needs **full** scope, not read-only.
- Source creation fails → check URL is a valid, accessible RSS/YouTube/Reddit URL.
- Adding group members → use `member_id` field, not `source_id`.
