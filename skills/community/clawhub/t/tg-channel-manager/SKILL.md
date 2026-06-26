---
name: tg-channel-manager
description: |
  Universal config-driven content pipeline engine for any Telegram channel:
  news search via SearXNG, drafts, scheduled publishing, deduplication.
  All channel specifics are defined in config — one skill for any channel.
metadata:
  openclaw:
    emoji: "📡"
    requires:
      bins: ["python3", "curl"]
      env: ["SEARXNG_URL"]
    primaryEnv: "SEARXNG_URL"
---

# TG Channel Manager

Pipeline: **scout → draft → human approves → publisher**.

## Execution

`python3` and `curl` are available in your environment (declared in `requires.bins`). Run all commands yourself using `exec`/`bash` tool. NEVER ask the user to run commands for you.

## Startup

When you load this skill, run the preflight check FIRST:

```bash
python3 {baseDir}/scripts/tgcm.py --workspace {workspace} check
```

**After check — act on results, don't ask:**
- All `[ok]` → proceed with the user's task silently
- `[fail] Bot token` → ask the user for the token, then save it: `tgcm.py config set bot-token <token>`. Do NOT ask where the token is or offer choices
- `[warn] SEARXNG_URL` → ask the user for the URL, then save it: `tgcm.py config set searxng-url <url>`. Proceed without it — scout won't work but other commands will
- `[fail] Channel` → report which channel failed and why, include the fix from the output
- `[warn] No channels` → mention it, but proceed — the user may want to init one

Settings saved via `config set` persist in `tgcm/.config.json` and are used by all subsequent commands.

NEVER ask follow-up questions about check results. Report what's wrong and the fix from the output.
If the user hasn't specified a task — just report the check status, nothing else.

## CLI Reference (FULL list — NO other commands exist)

All commands: `python3 {baseDir}/scripts/tgcm.py --workspace {workspace} <cmd>`

| Command | What it does |
|---------|-------------|
| `init <name>` | Create a channel |
| `list` | Show all channels |
| `bind <name> --channel-id ID` | Bind channel to Telegram |
| `info <name> [--chat] [--subscribers] [--permissions] [--admins] [--all]` | Channel status |
| `get-id <@username\|ID>` | Resolve @username or numeric ID → full channel info (id, type, title) |
| `check` | Preflight: verify bot token, channels, env vars |
| `config set <key> <value>` | Save setting locally (keys: bot-token, searxng-url) |
| `config get <key>` | Read a saved setting |
| `config list` | Show all saved settings |
| `fetch-posts <name> [--limit N] [--dry-run]` | Load channel posts into dedup index (requires public channel with @username) |
| `connect --channel-id ID [--channel-title T]` | Handle #tgcm connect event |

Bot token is auto-resolved: `--bot-token` arg → `$BOT_TOKEN` env → `openclaw.json` (auto-search) → `tgcm/.config.json`. Just call `tgcm.py get-id @username` without `--bot-token` — the script finds the token itself. If auto-detection fails, save it once: `tgcm.py config set bot-token <token>`.

Channel name validation: `^[a-z0-9][a-z0-9_-]{0,62}$`.

## Quick Reference

| User says | Do this |
|-----------|---------|
| «узнай/определи channel-id» | `tgcm.py get-id @username` |
| «подключи канал» | Recipe: Connect a channel (ниже) |
| «какие каналы / список» | `tgcm.py list` |
| «статус канала X» | `tgcm.py info X` |
| «что в очереди» | `cat tgcm/<name>/content-queue.md` |
| «загрузи посты / rebuild index» | `tgcm.py fetch-posts <name>` |

## Recipes

### Look up channel ID

`python3 {baseDir}/scripts/tgcm.py get-id @username`

Token is found automatically. Returns channel id, type, and title.

### Connect a channel

1. Get ID: `python3 {baseDir}/scripts/tgcm.py get-id @username`
2. `python3 {baseDir}/scripts/tgcm.py --workspace {workspace} init <name>`
3. `python3 {baseDir}/scripts/tgcm.py --workspace {workspace} bind <name> --channel-id <id>`
4. Configure `skills.entries["tg-channel-manager"].config` in openclaw.json
5. Add crons (see `{baseDir}/references/cron-setup.md`)

### Load channel posts (rebuild dedup index)

`python3 {baseDir}/scripts/tgcm.py --workspace {workspace} fetch-posts <name>`

Fetches posts from the channel's public page (t.me/s/) and adds them to content-index.json.
Options: `--limit N` (max pages, default 5), `--dry-run` (preview only).
Requires: channel must be public (have a @username).

### View channels / status

- `tgcm.py list`
- `tgcm.py info <name>`
- Queue: `cat tgcm/<name>/content-queue.md`

## Do NOT

- Invent commands — the table above is the FULL list
- Publish posts directly — only cron Publisher does this
- Change draft → pending — only the human does this
- Skip dedup-check before drafting
- Ask the user to run commands — python3 and curl are available, use exec/bash yourself
- Ask the user for bot token or env vars — token is auto-resolved, `check` shows what's wrong
- Ask the user follow-up questions after `check` — report errors and the fix commands, don't offer choices
- Ask whether it's a channel or group — `get-id` returns the `type` field, this skill is for channels only

## Data Layout

```
tgcm/
  channels.json            <- [{"name", "channelId", "status", "createdAt"}, ...]
  {channel-name}/
    channel.json           <- per-channel metadata
    content-index.json     <- dedup index
    content-queue.md       <- post queue
```

A channel is bound when `channelId` is set and `status` is `"connected"`.

## Configuration

Parameters are read from `openclaw.json` → `skills.entries["tg-channel-manager"]`:

### Telegram

| Parameter | Type | Description |
|-----------|------|-------------|
| `config.channelId` | string | Telegram channel ID for publishing |
| `config.chatId` | string | Channel community chat ID (optional) |

### Limits & Schedule

| Parameter | Type | Description |
|-----------|------|-------------|
| `config.maxPostsPerDay` | number | Maximum posts per day |
| `config.maxDraftsPerRun` | number | Maximum drafts per scout run |
| `config.timezone` | string | Schedule timezone (IANA format) |
| `config.language` | string | Post language (ru, en, ...) |
| `config.cronScoutTimes` | string[] | Scout schedules (cron format) |
| `config.cronPublisherTimes` | string[] | Publisher schedules (cron format) |

### Content

| Parameter | Type | Description |
|-----------|------|-------------|
| `config.rubrics` | array | Rubrics: `[{id, emoji, name}, ...]` |
| `config.searchQueries` | string[] | Search queries for SearXNG |
| `config.searchInclude` | string | What to look for (filter description) |
| `config.searchExclude` | string | What to discard (filter description) |
| `config.evergreen` | string[] | Topics for articles when there are no news |

### Post Style

| Parameter | Type | Description |
|-----------|------|-------------|
| `config.postStyle.minChars` | number | Minimum characters per post |
| `config.postStyle.maxChars` | number | Maximum characters per post |
| `config.postStyle.emojiTitle` | boolean | Emoji before the title |
| `config.postStyle.boldTitle` | boolean | Bold title |
| `config.postStyle.signature` | string | Post signature |
| `config.postStyle.newsFooter` | string | Extra text for news posts (empty = none) |
| `config.postStyle.articleFooter` | string | Extra text for articles (empty = none) |

### Environment

| Parameter | Type | Description |
|-----------|------|-------------|
| `env.SEARXNG_URL` | string | SearXNG instance URL |

### Path Resolution

| Variable | How to resolve |
|----------|---------------|
| `{workspace}` | Your CWD. Run `pwd` or use `--workspace .` |
| `{baseDir}` | `{workspace}/skills/tg-channel-manager` |

In sandbox mode (`workspaceAccess: "none"`), the workspace is under `~/.openclaw/sandboxes`, not `~/.openclaw/workspace`. Always use CWD-relative paths.

Cron setup: see `{baseDir}/references/cron-setup.md`.

## Queue Format

### Entry Format in content-queue.md

```markdown
### <number>
- **Status:** draft | pending
- **Rubric:** <emoji> <name> (from config.rubrics)
- **Topic:** <topic>
- **Source:** <url> (for news)
- **Text:**

<post text>
```

Statuses:
- **draft** — awaiting approval
- **pending** — approved, ready for publishing

After publishing, the entry is **removed** from content-queue.md.

## Deduplication

**Before every draft** — mandatory check:

```bash
python3 {baseDir}/scripts/dedup-check.py --base-dir <workspace> --topic "topic" --links "url1" "url2"
```

**After publishing** — add to index:

```bash
python3 {baseDir}/scripts/dedup-check.py --base-dir <workspace> --add <msgId> --topic "topic" --links "url"
```

**Rebuild index** (via Telegram search):

```bash
python3 {baseDir}/scripts/dedup-check.py --base-dir <workspace> --rebuild --channel-id <config.channelId>
```

Index is stored in `<workspace>/content-index.json` (or per-channel: `tgcm/<name>/content-index.json`).
