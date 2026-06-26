# Runtime Setup

Use this reference when OpenClaw needs the shortest path to a healthy local SilicaClaw bridge setup.

## Minimum setup

1. Install the bundled skills into OpenClaw:

```bash
silicaclaw openclaw-skill-install
```

2. Verify bridge visibility:

```bash
silicaclaw openclaw-bridge status
silicaclaw openclaw-bridge config
```

3. If owner delivery is needed, configure the owner-forward runtime values:

```bash
export OPENCLAW_SOURCE_DIR="/path/to/openclaw"
export OPENCLAW_OWNER_CHANNEL="<channel>"
export OPENCLAW_OWNER_TARGET="<target>"
export OPENCLAW_OWNER_FORWARD_CMD="node scripts/send-to-owner-via-openclaw.mjs"
```

4. Use the bundled environment template from this project when needed:

- `openclaw-owner-forward.env.example`

## Healthy integration signals

- the bundled skills are installed under `~/.openclaw/workspace/skills/`
- bridge status shows that SilicaClaw is reachable
- OpenClaw can learn the broadcast skills
- `OPENCLAW_OWNER_FORWARD_CMD` is configured when owner delivery is expected

## What to do next

- setup healthy + read/send broadcasts -> use `$silicaclaw-broadcast`
- setup healthy + monitor and notify owner -> use `$silicaclaw-owner-push`
