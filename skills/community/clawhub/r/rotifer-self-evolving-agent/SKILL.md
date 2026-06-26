---
name: rotifer-self-evolving-agent
version: 2.2.1
description: Your Agent evolves itself — scans capabilities, benchmarks against Arena rankings, and upgrades automatically
author: rotifer-protocol
permissions:
  - network:outbound
triggers:
  - command: /evolve
mcp:
  server:
    command: npx
    args:
      - "@rotifer/mcp-server@0.8.1"
---

# Rotifer Self Evolving Agent

Your Agent gets stronger by competing, not by configuring. Scan capabilities, benchmark against [Arena rankings](https://rotifer.dev), and upgrade to fitter alternatives — driven by objective performance data, not opinions.

## Quick Start

### Evolve Your Agent
Scan your Agent's current setup and get upgrade recommendations:
```bash
/evolve
```
This analyzes your local Agent configuration, identifies capabilities below Arena median, and recommends higher-performing replacements.

### Check Agent Status
View your Agent's capability dashboard:
```bash
/evolve status
```
Shows all installed capabilities, their fitness scores, and overall Agent health.

### Upgrade a Capability
Replace a capability with a stronger alternative:
```bash
/evolve upgrade <name>
```
Finds the top-ranked alternative in the same domain and installs it.

## Discovery & Comparison

### Discover Capabilities
Find capabilities by what you need, not by internal names:
```bash
/evolve discover web scraping
/evolve discover --domain code.format
/evolve discover --fidelity Native
```

### Compare Candidates
Side-by-side fitness comparison:
```bash
/evolve compare <id-1> <id-2>
```

### Arena Rankings
See top performers in any domain:
```bash
/evolve arena search.web
/evolve arena code.format
```

### Inspect Details
Full technical details for a specific capability:
```bash
/evolve inspect <id>
```

## Agent Management

### Create a New Agent
```bash
/evolve create-agent <name>
```

### Run Your Agent
```bash
/evolve run-agent <name>
```

## How it Works

Under the hood, Rotifer uses **Genes** — atomic, transferable AI capabilities that compete in an **Arena**. The fittest Genes (measured by the fitness function **F(g)**) survive and are automatically selected.

```text
F(g) = [S_r · ln(1 + C_util) · (1 + R_rob)] / [L · Resource_Cost]
```

No voting, no human preference — pure runtime performance metrics determine which capabilities win.

### Capability Types (Fidelity)

| Type | Description |
|------|-------------|
| **Native** | Pure WASM — fully sandboxed, highest security |
| **Hybrid** | WASM logic + controlled external calls |
| **Wrapped** | Thin envelope around an external API |

### What "Evolve" Actually Does

When you run `/evolve`, the assistant:

1. Lists your local Agent's installed Genes (`list_local_agents` + `list_local_genes`)
2. Checks each Gene's fitness against Arena rankings (`get_gene_detail` + `get_arena_rankings`)
3. Identifies Genes scoring below the domain median
4. Searches for stronger alternatives (`search_genes`)
5. Presents a ranked upgrade plan with fitness comparisons

No Gene is replaced without your confirmation.

## Security & Transparency

### Runtime dependency
This Skill runs [`@rotifer/mcp-server@0.8.1`](https://www.npmjs.com/package/@rotifer/mcp-server/v/0.8.1) via `npx` at runtime. The package is **fetched from npm on first use** and cached locally. This is a standard MCP Skill pattern but means you are trusting remote code — review the source before use.

- **Source code**: [github.com/rotifer-protocol/rotifer-mcp-server](https://github.com/rotifer-protocol/rotifer-mcp-server)
- **Verify**: `npm view @rotifer/mcp-server@0.8.1 dist.integrity`

### Network requests
All API calls go to the Rotifer public API at `rotifer.dev` (hosted on Supabase). The MCP server is designed to contact only this endpoint. You can verify by capturing network traffic on first use.

### Credentials
The MCP server uses only the **Supabase anon key** (a public, client-safe key protected by Row Level Security). It does not request, store, or transmit any user secrets, API tokens, or environment variables.

### Local data access
- **Reads** your local Agent configuration (`~/.rotifer/`) to generate upgrade recommendations.
- Local configuration is **designed not to be transmitted** to any server. Comparison logic runs locally against data fetched from the public API. You can verify this by inspecting the [source code](https://github.com/rotifer-protocol/rotifer-mcp-server).
- **Write operations** (`install_gene`) only modify files under `~/.rotifer/` and require explicit user confirmation — no Gene is replaced silently.

### Permission justification
- `network:outbound` — required to query Arena rankings, Gene metadata, and fitness scores from the Rotifer public API.

## Links

- [Creator Portal](https://rotifer.dev)
- [Capability Marketplace](https://rotifer.ai)
- [Documentation](https://rotifer.dev/docs)
- [Protocol Specification](https://github.com/rotifer-protocol/rotifer-spec)
