---
name: pubblue
description: >-
  Publish and visualize output via the pubblue CLI, with live P2P browser sessions.
license: MIT
compatibility: Requires Node.js 18+ with npm/pnpm/npx.
metadata:
  author: pub.blue
  version: "5.1.2"
allowed-tools: Bash(pubblue:*) Bash(npx pubblue:*) Bash(node:*) Read Write
---

# pubblue

Use this skill when the user asks about publishing, showing, or visualizing agent output on pub.blue.

## Required CLI Version

Use **pubblue CLI 0.6.9+**.

```bash
pubblue --version
npm i -g pubblue@latest
```

## Setup

```bash
# One-time auth
pubblue configure --api-key pub_KEY
# or
echo "pub_KEY" | pubblue configure --api-key-stdin
```

Key source: <https://pub.blue/dashboard>

By default, config is stored at `~/.openclaw/pubblue/config.json`.
Override config directory with `PUBBLUE_CONFIG_DIR` env var (useful in sandboxed environments).
For OpenClaw bridge mode, daemon runtime defaults to `OPENCLAW_WORKSPACE=~/.openclaw/workspace`.

## Core Commands

```bash
pubblue create page.html
pubblue create --slug demo --title "Demo" --public page.html
cat notes.md | pubblue create

pubblue get <slug>
pubblue get <slug> --content

pubblue update <slug> --file next.html
pubblue update <slug> --title "New title" --public

pubblue list
pubblue delete <slug>
```

Notes:
- Pub is built for agent-driven output sharing and live visualization.
- Pubs are **private by default**.
- `create` supports `--public/--private`, `--title`, `--slug`, `--expires`.
- `update` supports `--file`, `--title`, `--public/--private`, `--slug`.
- Content is optional: a pub can be live-only.

## Going Live

Live is browser-initiated: the user opens the pub page and clicks **Go Live**; the daemon answers.

1. Start the agent daemon:
```bash
pubblue start --agent-name "<agent-name>"
# optional explicit mode:
pubblue start --agent-name "<agent-name>" --bridge openclaw
pubblue start --agent-name "<agent-name>" --bridge claude-code
```

2. Check runtime status:
```bash
pubblue status
```

3. Send replies:
```bash
pubblue write "Hello"
pubblue write -c canvas -f /tmp/view.html
```

4. Read incoming (manual/debug):
```bash
pubblue read --follow -c chat
pubblue read --all
```

5. Stop daemon:
```bash
pubblue stop
```

6. Validate end-to-end:
```bash
pubblue doctor
pubblue doctor --wait-pong --timeout 30
pubblue doctor --skip-chat --skip-canvas
```

Important:
- `write` waits for delivery confirmation.
- `read` is consumptive; avoid multiple `read --follow` consumers on the same channel.

## Advanced Details (On Demand)

Only when needed:
- Show effective saved config: `pubblue configure`
- Inspect runtime and bridge state: `pubblue status`
- See command-specific options: `pubblue <command> --help`
