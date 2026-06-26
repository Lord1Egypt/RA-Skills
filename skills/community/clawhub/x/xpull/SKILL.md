---
name: xpull
description: "Pull tweets, threads, articles, and replies from X/Twitter. FxTwitter API primary (free), Grok x_search fallback (paid)."
metadata:
  openclaw:
    requires:
      bins: ["node"]
      env: ["XAI_API_KEY"]
    primaryEnv: "XAI_API_KEY"
    optional_env: ["GROK_DAILY_CAP"]
    repository: "https://github.com/sanjeevneo/xpull"
---

# xpull

## Scripts

- `node {baseDir}/scripts/fx-fetch.mjs "<url>"` — single tweet or article
- `node {baseDir}/scripts/fx-fetch.mjs "<url>" --thread` — thread (OP only, walks upward)
- `node {baseDir}/scripts/grok-x-search.mjs thread "<url>"` — full thread from root (requires XAI_API_KEY)
- `node {baseDir}/scripts/grok-x-search.mjs replies "<url>"` — replies (requires XAI_API_KEY)
- `node {baseDir}/scripts/grok-x-search.mjs search "<query>"` — search (requires XAI_API_KEY)
- `node {baseDir}/scripts/grok-x-search.mjs search "<query>" --from <handle>` — search by author (requires XAI_API_KEY)

## Configuration

| Variable | Required | Default | Description |
|---|---|---|---|
| `XAI_API_KEY` | For Grok features | — | xAI API key. Get one at [console.x.ai](https://console.x.ai). |
| `GROK_DAILY_CAP` | No | `20` | Max Grok calls per day. Resets at midnight UTC. |

Set `XAI_API_KEY` as an environment variable or in a `.env` file in the working directory.

## Notes

- `fx-fetch.mjs` — free, no credentials, no state. Calls `api.fxtwitter.com` only.
- `grok-x-search.mjs` — requires `XAI_API_KEY`. Writes `.grok-state.json` next to the script to enforce the daily cap. Calls `api.x.ai` only.
- Grok calls cost $5 per 1,000 `x_search` tool uses + token costs.

