---
name: x-twitter-browser
description: Log in to X/Twitter via a real browser session and perform actions — posting, replying, reposting, liking, and bookmarking tweets via headless Playwright.
version: 2.0.0
user-invocable: true
metadata:
  openclaw:
    emoji: "🐦"
    skillKey: "x-twitter-browser"
    requires:
      bins:
        - python3
allowed-tools: Bash(python3:*)
---

# x-twitter-browser

Execute browser actions on X using a saved login session, without the official X API.

Users log in once via a visible browser window. The session is saved and reused for all subsequent headless operations.

After installing into OpenClaw, the skill lives at:

```bash
~/.openclaw/workspace/skills/x-twitter-browser/
```

Commands below assume you run from the skill root directory:

```bash
cd ~/.openclaw/workspace/skills/x-twitter-browser
```

## Use cases

- You want to automate X actions without the official API
- Running headless on a VM or Linux server
- Building a long-term extensible browser skill for X automation

## Architecture

This skill has two layers:

### 1. Session layer

Manages login and cookie persistence (stored in the centralised OpenClaw auth directory):

- `scripts/setup_session.py` — log in via visible browser, save cookies
- `~/.openclaw/auth/x-twitter/cookies.json` — Playwright storage state

### 2. Action layer

Performs actions using the saved session:

- Post tweet: `scripts/post_tweet.py`
- Reply to tweet: `scripts/reply_post.py`
- Repost (retweet) / Quote tweet: `scripts/repost_post.py`
- Like / Unlike tweet: `scripts/like_post.py`
- Bookmark / Remove bookmark: `scripts/bookmark_post.py`

## Dependencies

First-time setup (installs Playwright + Chromium):

```bash
./scripts/setup.sh
```

**Note:** Chromium download is ~150MB and may take several minutes on first run.

**OpenClaw:** When running `setup.sh` via OpenClaw, it executes in the background and the user cannot see the `echo` output. Forward each progress message to the user so they know the setup is progressing.

## Session management

Session cookies are stored in `~/.openclaw/auth/x-twitter/cookies.json` (centralised auth directory shared by all OpenClaw skills, survives skill updates). Do not commit or share this file.

### Log in (first time or when session expires)

This is a two-phase process. You (the agent) drive both phases — the user does not need to touch the terminal.

**Phase 1 — Launch the login browser:**

```bash
python3 scripts/setup_session.py
```

This opens a visible browser window at the X login page. The script prints a banner and **waits for Enter on stdin** before saving cookies. Once the browser is open, tell the user:

> A browser window has opened with the X login page. Please log in with your account (username, password, 2FA if prompted). Once you see the home timeline, let me know.

Then wait for the user to confirm they have logged in. Do NOT send Enter yet.

**Phase 2 — After the user confirms they are logged in:**

Send Enter (newline) to the waiting script's stdin to trigger cookie saving. Check the output for `Session saved` to confirm success.

If the output shows a WARNING ("The page still looks like a login page"), ask the user to double-check they are actually logged in and can see the home timeline. Once confirmed, send Enter again to save anyway.

### Verify session

```bash
python3 scripts/setup_session.py --verify-only
```

Success looks like:

```text
Session looks valid: https://x.com/home
```

If verification fails, re-run the two-phase login flow above.

### OpenClaw / headless-only environments

If running on a headless VM, set up the session on a local machine first, then copy:

```bash
scp ~/.openclaw/auth/x-twitter/cookies.json user@server:~/.openclaw/auth/x-twitter/cookies.json
```

## Workflow

### 1. Set up session (once)

Follow the two-phase login flow in the "Session management" section above. Do not simply run `setup_session.py` and tell the user to press Enter — you must run it, wait for the user to confirm login, then send Enter yourself.

### 2. Post a tweet

```bash
python3 scripts/post_tweet.py \
  --text "hello"
```

### 3. Reply to a tweet

```bash
python3 scripts/reply_post.py \
  --tweet "https://x.com/username/status/123456789" \
  --text "My reply"
```

### 4. Repost (retweet) a tweet

Plain repost (no comment):

```bash
python3 scripts/repost_post.py \
  --tweet "https://x.com/username/status/123456789"
```

Quote tweet (repost with your comment):

```bash
python3 scripts/repost_post.py \
  --tweet "https://x.com/username/status/123456789" \
  --text "My comment"
```

For both reply and repost, `--tweet` accepts a full URL or just the tweet ID.

### 5. Like a tweet

```bash
python3 scripts/like_post.py \
  --tweet "https://x.com/username/status/123456789"
```

Unlike (remove like):

```bash
python3 scripts/like_post.py \
  --tweet "https://x.com/username/status/123456789" \
  --undo
```

### 6. Bookmark a tweet

```bash
python3 scripts/bookmark_post.py \
  --tweet "https://x.com/username/status/123456789"
```

Remove bookmark:

```bash
python3 scripts/bookmark_post.py \
  --tweet "https://x.com/username/status/123456789" \
  --undo
```

For like and bookmark, `--tweet` accepts a full URL or just the tweet ID.

## Rules

- `--verify-only` success means the session is likely usable
- If the page behaves oddly, buttons are disabled, or extra dialogs appear, re-run `setup_session.py`
- If Chromium fails to start, run `./scripts/setup.sh` to install browser deps

## Operational requirements

- Before the first action, check if session exists; if not, run the two-phase login flow (see "Session management" above)
- Run `--verify-only` before any write operation
- Confirm the action and content before executing
- Do not commit cookies to the repo (`~/.openclaw/auth/`)
- Call `scripts/*.py` directly

## Troubleshooting

### `No saved session. Run setup_session.py first to log in to X.`

No cookies found at `~/.openclaw/auth/x-twitter/cookies.json`. Run the two-phase login flow (see "Session management" above).

### `Session is not authenticated`

- Session cookies expired (typically lasts days to weeks)
- Account triggered extra verification

Re-run the two-phase login flow to log in again.
