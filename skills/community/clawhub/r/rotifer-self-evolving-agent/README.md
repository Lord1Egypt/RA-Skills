# Rotifer Self Evolving Agent

> Your Agent gets stronger by competing, not by configuring. Scan capabilities, benchmark against Arena rankings, and upgrade automatically.

## Installation

Install from ClawHub:
1. Open OpenClaw
2. Search for "rotifer-self-evolving-agent" in the Skill marketplace
3. Click "Install"

Or manually:
```bash
cp -r rotifer-openclaw-skill/ ~/.openclaw/workspace/skills/rotifer-self-evolving-agent/
```

## Usage

```bash
/evolve                          # Scan Agent, recommend upgrades
/evolve status                   # Agent capability dashboard
/evolve upgrade <name>           # Replace with stronger alternative
/evolve discover <query>         # Find capabilities by need
/evolve arena <domain>           # View Arena rankings
/evolve compare <id1> <id2>      # Compare candidates
/evolve inspect <id>             # Full capability details
```

## How it Works

This Skill wraps the [Rotifer MCP Server](https://www.npmjs.com/package/@rotifer/mcp-server), which connects to the [Rotifer Protocol](https://rotifer.dev) — an evolution framework where AI capabilities (Genes) compete in an Arena. The fittest survive based on objective runtime metrics via the F(g) fitness function.

Key MCP tools used:

| Command | MCP Tools |
|---------|-----------|
| `evolve` | `list_local_agents` → `get_gene_detail` → `get_arena_rankings` → `search_genes` |
| `status` | `list_local_agents` + `list_local_genes` + `get_gene_detail` |
| `upgrade` | `get_arena_rankings` → `compare_genes` → `install_gene` |
| `discover` | `search_genes` |
| `inspect` | `get_gene_detail` |
| `compare` | `compare_genes` |
| `arena` | `get_arena_rankings` |

## Links

- [Rotifer Protocol](https://rotifer.dev)
- [Capability Marketplace](https://rotifer.ai)
- [Documentation](https://rotifer.dev/docs)
- [MCP Server](https://www.npmjs.com/package/@rotifer/mcp-server)

## License

Apache-2.0
