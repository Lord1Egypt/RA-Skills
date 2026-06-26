---
name: twitter-listen-comment
description: Monitor one or more Twitter/X usernames via the 6551 API, generate a short humorous reply with `openclaw agent --json`, and submit the reply through an already logged-in Chrome X session. Use when creating or operating a reusable Twitter auto-listen-and-comment workflow, especially when you need: (1) watchlist-based polling, (2) 6551 tweet detection, (3) OpenClaw-generated reply text, (4) browser-driven commenting, or (5) notification messages for detected tweets and submitted comments.
---

Set up the skill as a reusable local automation package.

## Files
- Main script: `scripts/twitter_listen_comment.py`
- Start script: `scripts/run.sh`
- Config template: `references/config.example.json`
- Config notes: `references/config.md`

## Prepare config
Read `references/config.md` and create `references/config.json` from `references/config.example.json` before running.

## Run
Use one of these:

```bash
python3 scripts/twitter_listen_comment.py --config references/config.json --once
```

```bash
sh scripts/run.sh references/config.json
```

## Requirements
- Export `TWITTER_TOKEN`
- Ensure `openclaw` CLI is available in PATH, or set `OPENCLAW_BIN`
- Keep Chrome logged into X
- Keep the OpenClaw Chrome Relay attached on the tab when browser automation is required

## Behavior
- Poll watched usernames on an interval
- Ignore tweets older than `maxTweetAgeSeconds`
- Send a notice when a new eligible tweet is detected
- Generate a reply with `openclaw agent --json`
- Submit the comment with `openclaw agent --json`
- Send a second notice when comment submission succeeds
- Mark the tweet as processed only after submission succeeds

## Limits
- Success means comment submission succeeded, not deep post-verification
- Browser automation depends on Chrome Relay availability and X page state
- Notices route to the configured `notifyChannel` / `notifyTarget`
