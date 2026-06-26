---
name: x-bookmark-triage
description: >
  Automatically triages X/Twitter bookmarks into structured knowledge cards and posts them to a Discord channel (#knowledge-intake or similar). Captures tweet content via fxtwitter, scores relevance using Claude Haiku, assigns tier (1–10), freshness (evergreen/dated/expired), and topic tags, then optionally unbookmarks after capture. Includes a scheduled poll for new bookmarks, a one-time backlog sweep, and a manual drop handler. Use when: (1) setting up automated bookmark → knowledge card pipeline, (2) draining an existing bookmark backlog, (3) dropping a URL manually for immediate triage, (4) packaging this as a publishable skill for other OpenClaw users. Requires X OAuth 2.0 User Context with bookmark.read scope (+ bookmark.write to unbookmark). Triggers on: "triage my bookmarks", "set up bookmark pipeline", "drain bookmark backlog", "x-bookmark-triage", "knowledge intake".
---

# x-bookmark-triage

Turns X/Twitter bookmarks into searchable, tiered knowledge cards posted to a Discord channel. Captures, scores, and optionally unbookmarks — so your bookmark list stays clean and your knowledge base grows automatically.

> **Works standalone** — no OpenClaw required for core triage. OpenClaw integration is optional (adds scheduled polling via cron and bus events). See `references/adapting.md` for standalone setup.

## Architecture

```
X Bookmarks
    │
    ├── Scheduled poll (2×/day)  → bookmark-poll.js
    ├── Backlog sweep (one-time) → backlog-sweep.js
    └── Manual drop (on mention) → poll-channel.js (launchd poller)
                │
                ▼
        triage-url.js  (fetch → Claude Haiku → card)
                │
                ▼
    Discord #knowledge-intake  (structured card)
                │
                ▼
    X API DELETE /bookmarks/:id  (unbookmark)
```

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| X OAuth 2.0 app | [developer.x.com](https://developer.x.com) — Free tier works |
| Scopes | `bookmark.read` (required) + `bookmark.write` (for unbookmark) |
| Discord bot token | Needs `Send Messages` permission in target channel |
| Anthropic API key | `ANTHROPIC_DEFAULT_KEY` env var |
| Node.js 18+ | Scripts use `spawnSync`, no npm deps |

## Quick Start (8-step MVP)

1. **Get credentials:**
   - **X OAuth 2.0 app:** Create at [developer.x.com](https://developer.x.com) — Free tier. See `references/oauth-setup.md` for step-by-step.
   - **Discord bot token:** Create at [discord.com/developers](https://discord.com/developers/applications) — Bot needs `Send Messages` permission in your target channel.
   - **Anthropic API key:** From [console.anthropic.com](https://console.anthropic.com)

2. **Run auth flow:** `node scripts/x-oauth2-authorize.js` → saves refresh token to `data/x-oauth2-token-cache.json`

3. **Set env vars:** Export `X_OAUTH2_CLIENT_ID`, `X_OAUTH2_CLIENT_SECRET`, `X_OAUTH2_REFRESH_TOKEN`, `DISCORD_BOT_TOKEN`, `ANTHROPIC_DEFAULT_KEY`

4. **Set your Discord channel:** Set env var `KNOWLEDGE_INTAKE_CHANNEL_ID=<your-channel-id>` (preferred), OR edit `scripts/triage-url.js` line 19 to hardcode it.

5. **Test triage:** `node scripts/triage-url.js https://x.com/@username/status/1234567890 --source "manual drop"`

6. **Check Discord:** You should see a formatted card in your channel

7. **Verify dedup:** Run the command again — should skip (already seen)

8. **Done:** Your first card is live. Next: set up scheduling (see Steps 3–4 below)

---

## Setup

### 1. OAuth 2.0 Authorization

```bash
# Run the interactive auth flow
node scripts/x-oauth2-authorize.js
# → Opens browser, captures callback, saves to data/x-oauth2-token-cache.json
```

Store credentials in your gateway plist (or env):
```
X_OAUTH2_CLIENT_ID     — app OAuth 2.0 client ID
X_OAUTH2_CLIENT_SECRET — app OAuth 2.0 client secret
X_OAUTH2_REFRESH_TOKEN — from auth flow (auto-rotated by scripts)
```

The scripts also fall back to reading `refresh_token` from a secrets JSON file at runtime. See `references/oauth-setup.md` for full details.

### 2. Configure Target Channel

Set `CHANNEL_ID` at the top of `scripts/triage-url.js` to your Discord channel ID.

### 3. Register the Scheduled Poll (Optional — for automated polling)

```bash
# Register a cron job (9 AM + 5 PM daily)
# In OpenClaw: cron add — see references/cron-setup.md
# You can also run manually: node scripts/bookmark-poll.js
```

Alternatively, drain all bookmarks one-time:
```bash
node scripts/backlog-sweep.js --delay 3
```

### 4. Register the launchd Poller (Optional — for automated polling)

**Note:** `scripts/ai.watson.knowledge-intake-poll.plist` is a template. Customize it first:

1. Edit the file to replace `/PATH/TO/skills/x-bookmark-triage/scripts/poll-channel.js` with the actual path
2. Replace `YOUR_BOT_TOKEN`, `YOUR_ANTHROPIC_KEY`, `YOUR_CHANNEL_ID`, `/PATH/TO/workspace` with real values
3. Copy to LaunchAgents and load:

```bash
# After customizing the plist:
cp scripts/ai.watson.knowledge-intake-poll.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/ai.watson.knowledge-intake-poll.plist
```

Or use OpenClaw to manage it — see `references/cron-setup.md`.

## Scripts

### `triage-url.js` — Core triage engine

```bash
node scripts/triage-url.js <url> [--source "bookmark poll"|"manual drop"|"backlog sweep"]
```

- Fetches content (fxtwitter for tweets, markdown.new for web pages)
- Triages with Claude Haiku → produces tier, freshness, topic, tags, proposed action
- Posts formatted card to Discord
- Marks URL as seen in `data/knowledge-intake-seen.json`
- Exits 0 on success or "already seen"; exits 1 on hard failure

### `bookmark-poll.js` — Scheduled sweep (latest 20)

```bash
node scripts/bookmark-poll.js
```

- Refreshes OAuth token, fetches 20 most recent bookmarks
- Calls `triage-url.js` for each unseen URL
- Unbookmarks after successful triage (+ already-seen items)
- Emits `bookmark_sweep_complete` to bus

### `backlog-sweep.js` — One-time full drain

```bash
node scripts/backlog-sweep.js [--dry-run] [--limit 50] [--delay 3] [--no-unbookmark]
```

- Pages through ALL bookmarks (up to API limit)
- `--dry-run`: list URLs without triaging or unbookmarking
- `--limit N`: stop after N bookmarks
- `--delay N`: seconds between triage calls (default: 3)
- Emits `backlog_sweep_complete` to bus

### `poll-channel.js` — Discord drop handler

```bash
node scripts/poll-channel.js
# Or via wrapper: bash scripts/run-poll.sh
```

- Polls a Discord channel every 2 min for new messages
- Extracts URLs from message content
- Calls `triage-url.js` for each unseen URL
- Intended to run as a persistent launchd service

## Card Format

**Tier 3–10 (work-relevant):**
```
🗂️ **Title** @handle

• The Miracle: what's new/impressive
• Why it matters: connection to your work
• Key Features: [list]
• Proposed Action: specific next step
• Tier: 🥈 Tier 2 — Worth tracking (7/10) — relevance summary
• Freshness: 🌿 evergreen | Topic: #ai
• Tags: #tool #infra
• Link: <url>
```

**Tier 1–2 (off-topic/personal):**
```
📌 **Title** @handle — one-liner summary #personal <url>
```

## Tier Guide

| Tier | Label | Meaning |
|------|-------|---------|
| 9–10 | 🥇 Act now | Implement this week |
| 7–8 | 🥈 Worth tracking | Thread + investigate soon |
| 5–6 | 🥉 Knowledge doc | Revisit in a sprint |
| 3–4 | 📌 Low priority | Interesting, not actionable |
| 1–2 | 📌 Off-topic | Personal/entertainment — one-liner only |

## Freshness Values

- `evergreen` 🌿 — timeless, still valid in 2 years
- `dated` 📅 — relevant but will age (benchmarks, roadmaps)
- `expired` ⏰ — time-sensitive, likely already stale

## Topic Values (one per card)

`#ai` · `#veefriends` · `#product` · `#revenue` · `#openclaw` · `#personal` · `#x-strategy`

## Token / Cost Estimate

Each triage call: ~3.5K avg input + 300 output tokens (claude-haiku-4-5)
- Per URL: ~$0.003
- 20 new bookmarks/run: ~$0.06
- 2 runs/day at typical throughput: ~$3.60/month
- Full 1000-bookmark backlog: ~$3.50

## Seen-URL Deduplication

URLs are tracked in `data/knowledge-intake-seen.json`. Cap: 2,000 entries (FIFO). Bookmarks already in the seen cache are still unbookmarked — they were captured in a prior run.

## Refresh Token Rotation

X rotates refresh tokens on each use. The scripts:
1. Detect rotation (new token in response)
2. Save new token to `data/x-oauth2-new-refresh-token.txt`
3. Log a warning to update the plist env var

Watson auto-detects and updates the secrets file. For non-Watson deployments, monitor for this warning and update `X_OAUTH2_REFRESH_TOKEN` in your env.

## References

- `references/oauth-setup.md` — Full OAuth 2.0 setup walkthrough
- `references/cron-setup.md` — OpenClaw cron registration for scheduled polls
- `references/adapting.md` — How to adapt channel IDs, topics, triage prompt for your workspace
