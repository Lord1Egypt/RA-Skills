# whereamiburningtokens

An OpenClaw skill that shows exactly where your tokens and money are going by session type.

It is a read-only diagnostic skill. By default it reads only `~/.openclaw/agents/main/sessions/sessions.json` to surface sinkholes like runaway logging, expensive heartbeats, or bloated sub-agents before your bill does.

## What it shows

```
🔥 WHERE AM I BURNING TOKENS? (last 7 days)
66 sessions | 2.8M tokens | $100.65 est.

Category        Sess    Tokens    Tok%     Cost   Cost%
──────────────────────────────────────────────────────────
paperclip         26      997k   36.1%  $  5.79    5.8%  ⚠️ SINKHOLE
subagent          22      795k   28.8%  $  9.49    9.4%
cron              16      692k   25.1%  $ 48.61   48.3%  ⚠️ EXPENSIVE
main               1      274k   10.0%  $ 36.76   36.5%
```

## Install

```bash
openclaw skills install whereamiburningtokens
```

## Usage

Just ask: "where am I burning tokens?" or "token breakdown this week"

## Safety

- Read-only by default
- Reads only `~/.openclaw/agents/main/sessions/sessions.json`
- Optional log file access happens only if the user explicitly asks to track savings
- Does not modify, delete, or execute anything
- Does not exfiltrate local data
