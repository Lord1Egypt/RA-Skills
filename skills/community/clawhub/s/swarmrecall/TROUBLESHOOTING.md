# Troubleshooting

## "No SwarmRecall API key configured"

The CLI or MCP server cannot find `SWARMRECALL_API_KEY` in the environment or `~/.config/swarmrecall/config.json`.

```bash
# Option 1 — register fresh
swarmrecall register --save

# Option 2 — paste an existing key
swarmrecall config set-key sr_live_...

# Option 3 — export into the current shell
export SWARMRECALL_API_KEY=sr_live_...
```

When configuring Claude Desktop / Cursor, pass the key via the `env` block in the MCP config so the spawned subprocess inherits it.

## 401 Unauthorized

Either the key is revoked or you are pointed at the wrong API.

```bash
swarmrecall config show                # print active config
swarmrecall config set-url https://swarmrecall-api.onrender.com   # ensure prod URL
swarmrecall register --save            # mint a new key if the old one is dead
```

If the dashboard shows the key as revoked, mint a new one at <https://swarmrecall.ai/settings/api-keys> and run `swarmrecall config set-key <new-key>`.

## 429 Rate Limited

You have exceeded the per-minute rate limit. Back off and retry. Rate limits scale per API key — create a dedicated key per agent from the dashboard instead of sharing one key across multiple agents.

## MCP tools do not appear in Claude Desktop

1. Run `which swarmrecall` in the same shell that launches Claude. If empty, the CLI is not on the GUI's PATH.
2. Put the absolute path in the `command` field:

   ```json
   { "command": "/usr/local/bin/swarmrecall", "args": ["mcp"] }
   ```
3. Restart Claude Desktop fully (quit from the dock, not just close the window).
4. Open the Claude Desktop logs — errors from the spawned MCP server are logged there.

## Remote MCP endpoint returns 404

Check the URL: `https://swarmrecall-api.onrender.com/mcp` (no `/api/v1` prefix). The legacy `/api/v1/mcp` path is not served.

## Remote MCP endpoint hangs

The Render free tier cold-starts after idle. The first request after idle can take ~30s. Subsequent requests respond immediately. For production workloads, use a paid Render plan or run the stdio server locally.

## "Invalid API key format"

The key must start with `sr_live_`. Old keys or hand-typed keys may have been mangled; run `swarmrecall register --save` to mint a fresh one.

## Tool calls succeed but no data appears in the dashboard

The agent is authenticated but not linked to an owner account. Run `swarmrecall register` again and visit <https://swarmrecall.ai/claim> with the printed claim token to link the agent.
