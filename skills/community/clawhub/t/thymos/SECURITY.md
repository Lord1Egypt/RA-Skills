# Security Notes

Thymos is a local background daemon. Here's what it does and doesn't do with your system.

## What Thymos does

- Runs a local HTTP server on **port 7749** (localhost only, not exposed externally)
- Reads and writes JSON files under `./data/` (emotional state, memories, relationships)
- Sends HTTP requests to **Discord REST API** only if proactive messaging is configured (`config/proactive.json`) — opt-in, disabled by default
- Uses `pm2` to persist across reboots — this is intentional behavior for a 24/7 daemon

## What Thymos does NOT do

- No telemetry, analytics, or external data reporting of any kind
- No credentials, API keys, or environment variables are required for basic operation
- No postinstall scripts (`npm install` does not execute arbitrary code)
- No elevated privileges (runs as your user account)
- No inbound network exposure (port 7749 binds to `localhost` only)

## Data stored locally

| File | Contents | Retention |
|------|----------|-----------|
| `data/emotional_state.json` | Current neuromodulator values, mood vector | Overwritten every 30s |
| `data/relationships.json` | Per-user interaction counts, trust scores | Persistent |
| `data/emotional_memories.json` | Emotional episode log | Decays over time |
| `data/somatic_markers.json` | Decision-outcome history | Persistent |

Author IDs and message content fragments may be stored in these files for relationship modeling. Review and delete `data/*.json` at any time to reset.

## Verifying before install

```bash
# 1. Check for postinstall scripts
cat package.json | grep -A5 '"scripts"'

# 2. Check for network calls in source
grep -r "fetch\|axios\|http\|https" src/ --include="*.js" | grep -v "localhost\|127.0.0.1\|discord.com"

# 3. Audit npm dependencies
npm audit
```

## Pinned install (recommended)

```bash
git clone --branch v0.1.0 https://github.com/paperbags1103-hash/thymos
```

Using a tagged release ensures you're running reviewed code, not an unreviewed HEAD commit.
