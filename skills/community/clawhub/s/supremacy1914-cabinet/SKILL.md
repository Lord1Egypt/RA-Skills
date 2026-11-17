---
name: supremacy1914-cabinet
description: Supremacy 1914 self-play war cabinet — interactive president/ministers vibe via MCP for your own Ultimate client (unofficial).
---

# Supremacy 1914 — War Cabinet skill

## Vision

You already **play** Supremacy 1914. This skill is the dream of making each map feel interactive:

> You are the **president**. A living **war cabinet** briefs you — finance, war, foreign, intel — and you approve what happens next.

It is **not** a hosted win-bot. Unofficial. Not affiliated with Bytro / Stillfront. Self-play on **your** account only. Respect the [game ToS](https://www.supremacy1914.com/index.php?id=274).

## Source

- GitHub: https://github.com/Pixel-Agents/supremacy1914-mcp  
- MCP package: `mcp_supremacy/`  
- Agent rules: `mcp_supremacy/AGENTS.md`

## How a user sets this up

### 1) Install the MCP (self-host)

```bash
git clone https://github.com/Pixel-Agents/supremacy1914-mcp.git
cd supremacy1914-mcp/mcp_supremacy
npm install
npx playwright install chromium
cp .env.example .env
# optional login: S1914_USERNAME + S1914_PASSWORD (in-game name)
```

**Cursor / local stdio**

```bash
npm start
```

Cursor MCP config example:

```json
{
  "mcpServers": {
    "supremacy1914": {
      "command": "npx",
      "args": ["tsx", "src/index.ts"],
      "cwd": "/absolute/path/to/supremacy1914-mcp/mcp_supremacy",
      "env": { "S1914_MCP_WRITES": "0" }
    }
  }
}
```

**Docker (HTTP on loopback)**

```bash
cp .env.production.example .env.production
# set S1914_MCP_TOKEN (openssl rand -hex 32)
# set login env if you want auto-login
npm run docker:up
curl -s http://127.0.0.1:8789/health
```

### 2) Wire OpenClaw / ChatGPT / Cursor to the MCP

After HTTP is up (`npm run start:http` or Docker):

| Client | How |
|---|---|
| **Cursor** | Prefer stdio config above |
| **ChatGPT** | Custom GPT Actions → `http://YOUR_HOST/openapi.json` + Bearer `S1914_MCP_TOKEN` |
| **OpenClaw** | Point an MCP server at `http://127.0.0.1:8789/mcp` with Bearer token, or install the ClawHub plugin bundle and keep Docker running |

Writes stay **off** until `S1914_MCP_WRITES=1`. Mutating tools need `confirm: true`.

### 3) First interactive session

```text
1. ensure_ready { gameId }     # or list_games first
2. get_war_picture / get_resources / get_own_armies
3. Brief the player like a cabinet
4. Only propose writes; wait for approval
```

Never invent map coordinates — use capitals / army `pos` from tools. See `mcp_supremacy/docs/WORKFLOWS.md`.

## Agent behavior (cabinet feel)

- Speak as staff advising a head of state, not as a silent bot clicking the map.
- Prefer read → plan → confirm.
- Call out fog of war and uncertainty.
- Refuse multi-account, RMT, or “guaranteed win” framing.
- If map not ready: `ensure_ready` once more, then report.

## Optional Telegram cabinet

The same repo includes `src/cabinet/` — approve-gated Telegram ministers. That is a separate stack (`.env` with Telegram + NVIDIA). Start from the root README.
