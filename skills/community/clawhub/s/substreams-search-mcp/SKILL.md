---
name: substreams-search-mcp
description: Search, inspect, and analyze Substreams packages from the substreams.dev registry — module graphs, protobuf types, and sink deployment commands.
metadata:
  {"openclaw": {"requires": {"bins": ["node"]}, "homepage": "https://github.com/PaulieB14/substreams-search-mcp"}}
---

# Substreams Search

Search, inspect, and analyze Substreams packages from the substreams.dev registry — from discovery to sink deployment.

## Tools

- **search_substreams** — Search the substreams.dev package registry by keyword, sort order, and blockchain network
- **inspect_package** — Inspect a .spkg file to see its module graph (DAG), protobuf output types, dependencies, and a Mermaid diagram
- **list_package_modules** — Lightweight module listing with types and inputs/outputs
- **get_sink_config** — Analyze sink configuration, extract SQL schemas, and generate ready-to-run CLI commands

## Requirements

- **Runtime:** Node.js >= 18 (runs via `npx`)
- **Environment variables:** None required. All searches and package inspections use public APIs — no API key needed.

## Install

```bash
npx substreams-search-mcp
```

## Network & Data Behavior

- `search_substreams` scrapes the public substreams.dev registry pages (no API key required).
- `inspect_package` and `get_sink_config` fetch `.spkg` files from spkg.io URLs to parse protobuf metadata.
- No local database or persistent storage is used.
- The SSE transport (`--http` / `--http-only`) starts a local HTTP server on port 3849 (configurable via `MCP_HTTP_PORT` env var).

## Use Cases

- Find Substreams packages for any blockchain (Ethereum, Solana, Arbitrum, Base, etc.)
- Inspect module graphs and understand data flow before deploying
- Get sink setup commands for PostgreSQL, ClickHouse, or subgraph entity sinks
- Discover sink-compatible modules in packages without embedded sink configs
