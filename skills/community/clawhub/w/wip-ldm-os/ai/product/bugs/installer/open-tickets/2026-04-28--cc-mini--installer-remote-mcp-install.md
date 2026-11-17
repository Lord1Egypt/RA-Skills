# Installer: Remote MCP install action (interface #4)

**Date:** 2026-04-28
**Owner:** unassigned
**Status:** open
**Depends on:** [Remote MCP detection](2026-04-28--cc-mini--installer-remote-mcp-detection.md)
**Master plan:** [2026-04-28--cc-mini--installer-eight-interfaces-master-plan.md](2026-04-28--cc-mini--installer-eight-interfaces-master-plan.md)

## Contract (pinned)

> Remote MCP endpoint is declared by **package/catalog metadata** and registered by `ldm install`.

## What

After detection lands, `install.js` needs to register a detected Remote MCP endpoint. Local stdio MCP servers go in `.mcp.json` with `command` + `args`. Remote MCP is different: it points at an HTTPS URL and may need OAuth.

## Registration behavior

For a detected Remote MCP `{ url, transport, auth }`:

1. **Add to `~/.claude/.mcp.json`** as a remote entry:
   ```json
   {
     "<name>": {
       "url": "https://example.com/mcp",
       "transport": "streamable-http"
     }
   }
   ```
   The exact key shape depends on Claude Code's current `.mcp.json` schema for remote MCP. Verify before shipping; if Claude Code does not yet accept remote in `.mcp.json`, fall back to printing instructions only and gating registration on a flag.

2. **Print a Claude Desktop hint:** Claude Desktop's connector UI is where remote MCPs are added by users. The installer should print one line: *"To use this in Claude Desktop, add `<url>` under Connectors."* It should NOT modify Claude Desktop's config (different process, different sync model, user opt-in).

3. **Honor `--dry-run`:** show the planned write without making it.

## Auth assumptions

- `auth: "none"` ... write the URL as-is. Useful for internal/dev endpoints.
- `auth: "shared-secret"` ... installer prompts the user once (or reads from 1Password if a hint is given), stores under a per-product key in a sealed config file (NOT in `.mcp.json` plaintext if avoidable).
- `auth: "oauth"` ... first cut: print a TODO, do not attempt OAuth. We will wire the OAuth handshake in a follow-up ticket once we have one real Remote MCP product anchoring the flow. Memory Crystal is the likely first.

## How this differs from local MCP install

| Step | Local MCP (#3) | Remote MCP (#4) |
|------|----------------|-----------------|
| Where it goes | `.mcp.json` `command` + `args` | `.mcp.json` `url` + `transport` |
| Process lifecycle | Spawned per session | None (server is remote) |
| First-run setup | None | Possibly OAuth or shared secret |
| Removal | Drop the entry | Drop the entry; revoke OAuth if applicable |
| Surfaces it lights up | Claude Code, Cursor, OpenClaw | Claude Desktop, web, mobile |

## Acceptance

- `ldm install <slug>` for a product with Remote MCP declared writes the URL into `.mcp.json` and prints the Claude Desktop hint.
- `ldm install --dry-run <slug>` shows the planned write without making it.
- A test fixture proves install + dry-run.
- Removal works: `ldm install` against a manifest that no longer declares Remote MCP cleans the entry.

## Open questions

- Does `.mcp.json` currently support a remote URL entry, or do we need to wait on Claude Code remote MCP support? If we wait, ship the detection first and gate registration behind a `--remote-mcp-experimental` flag.
- Which of our products ships a Remote MCP first? Memory Crystal is the obvious candidate (search memory from a phone via Claude Desktop). That decision is its own ticket, not this one.
