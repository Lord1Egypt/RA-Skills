---
name: twitter-thread-scheduler
version: 1.0.0
description: Post native X/Twitter threads by chaining reply-to calls via Twitter
  API v2. Buffer cannot post threads — use this for any multi-tweet X content from
  the content pipeline.
author: loki
tags:
- twitter
- x
- threads
- social
- scheduling
- content-pipeline
created: 2026-04-03
metadata:
  openclaw:
    emoji: 🧵
    primaryEnv: TWITTER_ACCESS_TOKEN
    requires:
      bins:
      - python3
      env:
      - TWITTER_ACCESS_TOKEN
    network:
      outbound: true
      reason: Posts tweets and thread replies via Twitter API v2.
---

# Twitter Thread Scheduler

## Why This Exists

Buffer's GraphQL API has no `thread` field — it only supports single posts. To post a proper X thread (tweet 1 → reply → reply → ...), you need direct Twitter API v2 access.

This script uses the `redditech` OAuth2 credentials from `~/.xurl` to:
1. Post tweet [1/N] — get back the tweet ID
2. Post tweet [2/N] as `reply: { in_reply_to_tweet_id: <id> }` — get tweet 2's ID
3. Continue through the queue until all N tweets are posted
4. Log all tweet IDs + URLs to `memory/thread-log.jsonl`

**This is the ONLY way to schedule real X threads.** Always use this script over Buffer for multi-tweet content.

---

## Script

```
scripts/tweet_thread_scheduler.py
```

Auth: `~/.xurl` → `apps.redditech.users.redditech.access_token` (auto-refreshes on 401)

---

## Commands

### Preview (parse + char check, no posting)
```bash
python3 scripts/tweet_thread_scheduler.py preview \
  --file projects/social-growth/thread-<slug>.md
```
Run this first. Confirms tweet count and flags any over 280 chars.

### Post immediately
```bash
python3 scripts/tweet_thread_scheduler.py post \
  --file projects/social-growth/thread-<slug>.md \
  --slug <slug>
# Prompts for confirmation before posting
```

### Dry run
```bash
python3 scripts/tweet_thread_scheduler.py post \
  --file projects/social-growth/thread-<slug>.md \
  --slug <slug> \
  --dry-run
```

### Schedule for later (ISO8601 datetime)
```bash
python3 scripts/tweet_thread_scheduler.py schedule \
  --file projects/social-growth/thread-<slug>.md \
  --slug <slug> \
  --at "2026-04-05T08:00:00+11:00"
# Writes queue file + creates `at` job
```

### Fire a queued thread (called automatically by `at`)
```bash
python3 scripts/tweet_thread_scheduler.py fire \
  --queue memory/thread-queue/<slug>.json
```

---

## Thread File Format

The script parses the blog-to-social output format automatically:

```markdown
## Thread (9 tweets)

[1/9] First tweet text here.

[2/9] Second tweet text here.

...

[9/9] Final tweet with blog URL. #Hashtag1 #Hashtag2
```

Also supports `## Tweet N` headers and `---` dividers.

**Always run `preview` before scheduling** to confirm parsing is correct.

---

## Rate Limits

- 3 second delay between tweets in a thread
- Auto-retry with exponential backoff on HTTP 429
- Twitter free tier: 300 write operations per 15 minutes
- A 9-tweet thread uses 9 write ops — well within limits

---

## Queue & Logs

| Path | Purpose |
|---|---|
| `memory/thread-queue/<slug>.json` | Queued thread data (tweets + schedule time) |
| `memory/thread-log.jsonl` | Posted threads — all tweet IDs + URLs |

---

## Integration with Content Pipeline

In the blog-to-social and blog-publish playbooks:
- Sara produces `projects/social-growth/thread-<slug>.md`
- Run `preview` to verify parsing
- Replace `[BLOG_URL]` placeholder before scheduling
- Use `schedule --at <publishAt + 15min>` to align with blog embargo timing
- LinkedIn single posts → still use `scripts/buffer-post.mjs`

**Rule:** Buffer for LinkedIn. This script for X threads.

---

## Lessons Learned

**2026-04-03 — First use (portkey-patterns + ollama-embeddings):**
- Buffer `createPost` with `thread` field returns `GRAPHQL_VALIDATION_FAILED` — field doesn't exist
- Workaround: built this script using Twitter API v2 `reply` field
- `at` scheduling works cleanly — jobs survive across sessions
- 3s inter-tweet delay is sufficient for free tier rate limits
- Both threads (9 tweets + 8 tweets) parse cleanly from `[1/N]` format

**Buffer delete API (corrected 2026-04-03):**
- Input field: `id` (NOT `postId`)
- Response union: `DeletePostSuccess { id }` | `VoidMutationError { message }` (NOT `PostActionSuccess`)
- This is different from `createPost` which uses `PostActionSuccess`
