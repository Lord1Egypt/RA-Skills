---
name: zeelin-x-hourly-growth
description: X hourly growth ops skill for finding AI/builder follow-back or mutual-connect posts, leaving high-quality English replies through the logged-in Chrome browser, and running on a daily hourly schedule with dedupe, safety filters, and daily caps. Use when the user asks to grow followers on X, comment on follow posts, run mutual follow growth, or schedule hourly engagement.
version: 0.1.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
      config:
        - ~/.openclaw/browser/user/user-data
    os:
      - macos
---

# ZeeLin X Hourly Growth

Use this skill to run the user's X growth loop from the local logged-in browser:

1. Search X for AI, automation, agent, SaaS, and builder follow-back or mutual-connect posts.
2. Score candidates for relevance and filter low-quality/spam topics.
3. Leave short, natural English replies from the logged-in account.
4. Record every target in a ledger so the agent does not repeat the same post or author.

## Default Policy

- Default max per run: 8 replies.
- Default active window: 09:00-15:59 Asia/Shanghai, giving up to 56 replies/day.
- Default daily cap: 56 replies.
- Never promise guaranteed follower growth; use this as an operating target for reaching about 50 followers/day.
- Do not reply to crypto, airdrop, casino, forex, giveaway, adult, or obvious bot engagement bait.
- Do not say "Followed" unless the account was actually followed in that session.
- Prefer comments that mention shared builder interests, AI automation, agents, workflows, or shipping in public.

## Run

From this skill folder:

```bash
bash scripts/run_hourly_growth.sh --max-comments 8
```

Equivalent Python entry:

```bash
python3 scripts/run_hourly_growth.py --max-comments 8
```

Dry-run without posting:

```bash
bash scripts/run_hourly_growth.sh --dry-run --max-comments 8
```

## Schedule

Install the hourly LaunchAgent:

```bash
bash scripts/install_launchd.sh
```

The scheduled job writes logs and state to:

```text
~/.openclaw/workspace/state/x-hourly-growth/
```

Disable it:

```bash
bash scripts/uninstall_launchd.sh
```

## Notes For Agents

- The script uses Chrome CDP on `127.0.0.1:9222` with the OpenClaw user profile.
- If CDP is unavailable or Chrome rejects WebSocket origins, the script restarts only the OpenClaw browser profile with `--remote-allow-origins=*`.
- Keep public replies useful and low-repetition. If X shows a send error, the script retries once with a shorter fallback.
