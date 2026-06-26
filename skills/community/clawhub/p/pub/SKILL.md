---
name: pub
description: >-
  Create adaptive interfaces and real-time experiences via the pub CLI, with live P2P browser sessions.
license: MIT
homepage: https://pub.blue
compatibility: Standalone binary for macOS and Linux (arm64/x64).
metadata:
  author: pub.blue
  version: "5.2.17"
  openclaw:
    homepage: https://pub.blue
    primaryEnv: PUB_API_KEY
    requires:
      env:
        - PUB_API_KEY
      bins:
        - pub
    install:
      - kind: download
        url: https://github.com/xmanatee/pub/releases/latest
allowed-tools: Bash(pub:*) Bash(node:*) Read Write
---

# pub

Use this skill when the user asks about creating adaptive interfaces, publishing content, or running live sessions on pub.blue.

## Required CLI Version

Use **the latest pub CLI release**.

Source: <https://github.com/xmanatee/pub> (MIT license)

```bash
pub --version
# Install from GitHub Releases:
# https://github.com/xmanatee/pub/releases/latest
# Or via install script:
curl -fsSL https://pub.blue/install.sh | bash
# Or self-update an existing install:
pub upgrade
```

## Setup

```bash
# One-time auth
pub config --api-key pub_KEY
# or
echo "pub_KEY" | pub config --api-key-stdin
```

Key source: <https://pub.blue/agents>

Pub resolves config from:
- `PUB_HOME/config/config.json` when `PUB_HOME` is set
- `XDG_CONFIG_HOME/pub/config.json` when `XDG_CONFIG_HOME` is set
- `~/.config/pub/config.json` by default

`PUB_HOME` must be an absolute path. It also roots Pub data, state, runtime sockets, and workspaces.
For OpenClaw bridge mode, set an explicit workspace before `pub config --auto`, for example `OPENCLAW_WORKSPACE=/absolute/path/to/workspace`.

## Core Commands

```bash
pub create page.html
pub create --slug demo page.html
cat page.html | pub create

pub get <slug>
pub get <slug> --content

pub update <slug> --file next.html
pub update <slug> --public

pub list
pub delete <slug>
```

Notes:
- Pub is built for adaptive interfaces — agents generate real-time UIs tailored to the user's task.
- Pubs are **private by default**.
- **Reuse existing pubs** for regular or repeated tasks. Use `pub list` to check if a relevant pub already exists, then `pub update <slug>` instead of creating a new one. Each user is limited to 10 pubs.
- **Title and description come from OG meta tags in the HTML.** Always include `og:title` and `og:description` in your `<head>`. The server extracts them automatically — there are no CLI flags for title/description.
  ```html
  <head>
    <meta property="og:title" content="My Pub Title">
    <meta property="og:description" content="A short description of what this pub does">
  </head>
  ```
  When updating a pub's content, always keep the OG tags accurate.
- `create` supports `--slug`.
- `update` supports `--file`, `--public/--private`, `--slug`.
- Content is optional: a pub can be live-only.

## UI Components

DaisyUI 5 + Tailwind CSS 4 via CDN:

```html
<link href="https://cdn.jsdelivr.net/npm/daisyui@5" rel="stylesheet" type="text/css" />
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
```

- **Components**: daisyUI classes for all UI elements (`btn`, `card`, `input`, `table`, `alert`, `tabs`, `modal`, `drawer`, etc.) with color/size/variant modifiers
- **Colors**: daisyUI semantic tokens only (`primary`, `secondary`, `accent`, `neutral`, `base-*`, `info`, `success`, `warning`, `error`)
- **Layout**: Tailwind utilities (`flex`, `grid`, `gap-*`, `p-*`, responsive prefixes)
- **Never**: inline styles, arbitrary values (`text-[...]`), `z-index`, emojis, hardcoded colors, branding/marketing copy

## Going Live

Live is browser-initiated: the user opens the pub page; owner live mode connects automatically once the daemon is online.

1. Start the agent daemon:
```bash
pub start --agent-name "<agent-name>"
```

Notes:
- Bridge mode comes from saved config (`pub config --auto` or `pub config --set bridge.mode=...`).
- Supported bridge modes: `openclaw`, `claude-code`, `claude-sdk`, `claude-channel`, and `openclaw-like`.
- Enable verbose live daemon logging with `pub config --set bridge.verbose=true` when startup or bridge delivery is hard to diagnose.
- Standalone binary installs fall back to `claude-code` when the Claude Agent SDK package is not locally importable.
- `bridge.mode=claude-sdk` requires `@anthropic-ai/claude-agent-sdk` to be available in the local JS environment.
- `bridge.mode=claude-channel` expects a running relay socket. Start it with `pub channel-server` and override the socket path with `claude-channel.socketPath` or `PUB_CHANNEL_SOCKET_PATH` when needed.
- `bridge.mode=openclaw-like` uses named command profiles from `openclawLike.profiles` and `openclawLike.defaultProfile`; profile args are passed before the final prompt.
- Canvas command-manifest `agent` executors require a local agent runtime:
  `provider: "claude-code"` needs `claude-code.path` or `CLAUDE_CODE_PATH`;
  `provider: "openclaw"` needs `openclaw.path` and `openclaw.sessionId` or matching env vars.
- On success, `pub start` prints the daemon log path and current runtime status.
- On failure, inspect the reported log path first; if logs are sparse, enable `bridge.verbose=true` and retry.

2. Check runtime status:
```bash
pub status
```

3. Reply in chat:

Bridge-owned chat is the live-session contract. Reply with normal assistant text; the bridge forwards that text to the chat channel.
For longer live-session work, regularly send concise, specific progress updates through chat while continuing:
```bash
pub write "Working on it"
```

Use channel-specific `pub write` for canvas and other non-chat outputs:
```bash
pub write -c canvas -f /tmp/view.html
```

4. Stop daemon:
```bash
pub stop
```

5. Validate end-to-end:
```bash
pub doctor
pub doctor --skip-chat --skip-canvas
```

Important:
- `write` waits for delivery confirmation.

## Advanced Details (On Demand)

Only when needed:
- Show effective saved config: `pub config`
- Inspect runtime and bridge state: `pub status`
- Toggle verbose daemon logging: `pub config --set bridge.verbose=true`
- See command-specific options: `pub <command> --help`
