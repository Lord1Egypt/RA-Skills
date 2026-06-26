# Installer: Remote MCP detection (interface #4)

**Date:** 2026-04-28
**Owner:** unassigned
**Status:** open
**Master plan:** [2026-04-28--cc-mini--installer-eight-interfaces-master-plan.md](2026-04-28--cc-mini--installer-eight-interfaces-master-plan.md)

## Contract (pinned)

> Remote MCP endpoint is declared by **package/catalog metadata** and registered by `ldm install`.

Anything fuzzier than that is out of spec. No filesystem-sniffing for "maybe this is HTTP" inferences. The repo declares it. The catalog confirms it. The installer registers it.

## What

`detect.mjs` (in both `wip-ldm-os-private/lib/install/` and the toolbox copy at `tools/wip-universal-installer/detect.mjs`) does not know how to detect a Remote MCP declaration. Today it detects six interfaces; CC Plugin landed in the toolbox in March; Remote MCP has never landed.

## How Remote MCP differs from local MCP (#3)

| Aspect | Local MCP (#3) | Remote MCP (#4) |
|--------|----------------|-----------------|
| **Transport** | stdio (child process) | HTTPS + SSE or streamable HTTP |
| **Process model** | Spawned by Claude Code per session | Long-running server, multi-tenant |
| **Discovery** | `mcp-server.{mjs,js,ts}` file at repo root | `mcp.remote` field in `package.json` (preferred) |
| **Registration** | `command` + `args` in `.mcp.json` | `url` (+ `transport`, `auth`) in `.mcp.json` |
| **Auth** | Trust the local process | OAuth or shared secret over HTTPS |
| **Surface** | Claude Code, Cursor, OpenClaw (local agents) | Claude Desktop connectors, web, mobile |

This is why Remote MCP gets its own interface number, not a flag on #3.

## Convention

A repo declares Remote MCP via `package.json`:

```json
{
  "mcp": {
    "remote": {
      "url": "https://example.com/mcp",
      "transport": "streamable-http",
      "auth": "oauth"
    }
  }
}
```

`url` may be a placeholder (`"https://__DEPLOYED_URL__"`) for products that ship the code in the repo and the URL via deploy. In that case the catalog entry resolves the real URL at install time (see Catalog/install metadata below).

## Detection rule

```
Detect remoteMcp if:
  package.json contains a top-level `mcp.remote.url` string.
```

Single rule. No file-pattern fallback. The repo author opts in by writing the field.

## Catalog/install metadata

Each `catalog.json` entry for a product that ships Remote MCP gains:

```json
{
  "id": "memory-crystal",
  "remoteMcp": {
    "url": "https://memory.wip.computer/mcp",
    "transport": "streamable-http",
    "auth": "oauth"
  }
}
```

If `package.json.mcp.remote.url` is a placeholder, the catalog entry's URL wins. Otherwise the package.json value is authoritative.

## Acceptance

- `detect.mjs` returns `remoteMcp` in the interface list when `package.json.mcp.remote.url` is set.
- `detectInterfacesJSON()` includes `{ remoteMcp: { url, transport, auth } }`.
- A test fixture under `examples/remote-mcp/` proves the detector works.
- Detector returns nothing for a repo that only has local stdio MCP (no false positive on #3).

## Linked

- [Remote MCP install action](2026-04-28--cc-mini--installer-remote-mcp-install.md) (depends on this)
- [Catalog audit for install-spec URL field](2026-04-28--cc-mini--catalog-install-spec-url-audit.md) (related; same catalog.json schema)
