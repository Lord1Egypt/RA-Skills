---
name: "wyze-scale"
description: "Read body metrics from a Wyze smart scale — weight, BMI, body fat, water, muscle, BMR. Supports multiple household members. Unofficial Wyze API via wyze-node."
homepage: "https://github.com/noelportugal/wyze-node"
metadata:
  openclaw:
    emoji: "⚖️"
    requires: { bins: ["node"] }
---

# Wyze scale (body metrics)

Read body-composition data from a Wyze smart scale via the bundled `scale` CLI,
which wraps [`wyze-node`](https://www.npmjs.com/package/wyze-node). Reuses the
same cached login as the `wyze` skill (no password).

> Unofficial: `wyze-node` uses Wyze's developer API Key auth and
> reverse-engineered endpoints. Not affiliated with or endorsed by Wyze; Wyze
> may change their API at any time.

## When to use
Questions about weight or body composition: "what's my weight", "what's my
BMI / body fat", "am I down since last time", weigh-in history/trend. A single
scale can hold several people — scope a reading to a specific member by name.

## Setup (once)
This skill shares the `wyze` skill's setup. If you haven't already:
1. Install the dependency: `npm install --prefix "{baseDir}/scripts" wyze-node`
   (or have `wyze-node` installed globally, or set `WYZE_NODE_DIR` to a clone).
2. Put `WYZE_EMAIL`, `WYZE_KEY_ID`, `WYZE_API_KEY` in `WYZE_ENV`
   (default `~/.openclaw/secrets/wyze.env`) — keys from
   https://developer-api-console.wyze.com/#/apikey/view
3. Cache a login token in a terminal once, using the `wyze` skill's `login`
   command (the token is shared between both skills).

## Run
```
node "{baseDir}/scripts/scale" [latest|history|users] [args]
```

- `latest [user]` (default) — most recent weigh-in: weight (kg + lb), BMI, body
  fat, body water, muscle, BMR, metabolic age, date, and change vs the prior
  reading. Pass a member name or id to scope it.
- `history [n] [user]` — last `n` weigh-ins (default 7) with weight + date,
  optionally for one member.
- `users` — list members the scale knows about (or the raw user ids seen in
  records if no named members are configured).

`<user>` is a case-insensitive substring of a member's nickname, or a raw
member id. Omit it to use the most recent weigh-in regardless of member.

## Configuration (shared with the `wyze` skill)
- `WYZE_NODE_DIR` (default `~/code/wyze-node`) or an npm-installed `wyze-node`
- `WYZE_ENV` (default `~/.openclaw/secrets/wyze.env`) — `WYZE_EMAIL`,
  `WYZE_KEY_ID`, `WYZE_API_KEY`
- `WYZE_TOKEN_DIR` (default: `WYZE_NODE_DIR` if present, else `~/.openclaw/wyze`)

## Privacy
Body metrics are sensitive personal data. Share a reading only with its owner in
a private/direct session — never surface anyone's weight or body composition in
group chats or shared surfaces.

## Notes
- The scale device is `product_type` WyzeScale. Weight is stored in kg; the CLI
  also prints pounds.
- Backed by `wyze-node`. If calls fail with auth errors, re-run the `wyze`
  skill's `login` to refresh the cached token.
- License: MIT. Backed by the open-source `wyze-node` client.
