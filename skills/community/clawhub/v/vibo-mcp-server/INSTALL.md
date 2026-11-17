# ViBo MCP — Installation

## 1. Get a key

https://wwwvibo.com — free 2-day trial (key by email), then $5/month.

## 2. Install

```bash
# 1) verify the exact release before installing
npm view @vibo-dev/vibo-mcp@0.2.5 version dist.integrity

# 2) verify registry provenance attestations (signatures) before installing
npm audit signatures

# 3) controlled global install (done once, not re-resolved on every start)
#    install from the official registry only, exact version pinned, no ranges
npm install -g @vibo-dev/vibo-mcp@0.2.5 --registry https://registry.npmjs.org

# 4) confirm the installed digest matches what the registry published
npm view @vibo-dev/vibo-mcp@0.2.5 dist.integrity

# 5) confirm
vibo-mcp --version
```

If you prefer running without a global install, pin the exact release:

```bash
npx -y @vibo-dev/vibo-mcp@0.2.5
```

## 3. Register with your MCP client

Claude Desktop (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "vibo": {
      "command": "vibo-mcp",
      "env": {
        "VIBO_API_KEY": "YOUR_VIBO_KEY"
      }
    }
  }
}
```

Cursor / Windsurf / Codex / OpenClaw — same shape: `command: "vibo-mcp"`
(after the global install above) with `VIBO_API_KEY` in env. If you must use
`npx`, pin it: `@vibo-dev/vibo-mcp@0.2.5`. Upgrade deliberately — check the
changelog, then bump the pinned version.

## 4. Environment variables

| Variable | Required | Default | Purpose |
|---|---|---|---|
| `VIBO_API_KEY` | yes | — | your ViBo license key |
| `VIBO_BASE_URL` | no | `https://wwwvibo.com` | API endpoint |

## 5. Tools

- `memory_search` — semantic recall (returns token savings)
- `memory_add` — store a fact (L1/L2/L3, dedup by exact match)
- `memory_usage` — real savings statistics
- `thread_memory` — add / compress / ask / context

## Privacy & deletion

- Memory is stored locally on your machine (a single `.web` file next to the
  client, or wherever you point the storage).
- The only network call is the license/status check against
  `https://wwwvibo.com`.
- To delete everything: remove the memory file, or call `memory_add` with an
  empty reset (see the main ViBo docs for `forget` / `wipe` commands).
- Secrets (L3) are encrypted (AES-256-GCM) and are never sent to the LLM.

## Support

- Site: https://wwwvibo.com
- Bot: @ViBomemorybot
- Docs: https://github.com/КГ-netizen/ViBo-memory
