# UPLO Clinical — Drug-to-Patient Intelligence

AI-powered clinical operations intelligence spanning pharmaceutical development and healthcare delivery. Unified search across clinical trials, protocols, and patient care documentation.

[![ClawHub](https://img.shields.io/badge/ClawHub-uplo-clinical-blue)](https://clawhub.com/skills/uplo-clinical)
[![MCP](https://img.shields.io/badge/MCP-21_tools-green)](https://uplo.ai)
[![Schemas](https://img.shields.io/badge/schemas-15-orange)](https://uplo.ai/schemas)

## Quick Install

```bash
clawhub install uplo-clinical
```

Or add to your Claude Desktop config:

```json
{
  "mcpServers": {
    "uplo-clinical": {
      "command": "npx",
      "args": ["-y", "@agentdocs1/mcp-server", "--http"],
      "env": {
        "AGENTDOCS_URL": "https://your-instance.uplo.ai",
        "API_KEY": "your-api-key",
        "DEFAULT_PACKS": "pharma,healthcare"
      }
    }
  }
}
```

## What You Get

- **15 industry schemas** — pre-built extraction templates for Clinical documents
- **21 MCP tools** — search, GraphRAG, directives, knowledge gaps, proposals, and more
- **1,400+ format support** — PDF, DOCX, PPTX, emails, images, and 1,400 more via Docling + Tika
- **Classification tiers** — public/internal/confidential/restricted access control
- **Benchmark proven** — 96% accuracy vs 53% for raw context at scale

## MCP Tools Available

| Tool | Description |
|------|-------------|
| `search_knowledge` | Semantic search across extracted knowledge |
| `search_with_context` | GraphRAG: vector search + entity resolution + edge traversal |
| `export_org_context` | Full organizational context snapshot |
| `get_directives` | Strategic priorities and directives |
| `find_knowledge_owner` | Find subject matter experts |
| `propose_update` | Suggest knowledge base updates |
| `report_knowledge_gap` | Flag missing information |
| `flag_outdated` | Mark stale entries |

## Schema Packs

- **Pharma** — 5 schemas
- **Healthcare** — 10 schemas

## Related Skills

- [UPLO Healthcare — Clinical Protocol Intelligence](https://clawhub.com/skills/uplo-healthcare) — AI-powered healthcare knowledge management.
- [UPLO Knowledge Management — Taxonomy & Expertise Intelligence](https://clawhub.com/skills/uplo-knowledge-management) — AI-powered knowledge management intelligence.
- [UPLO Pharma — Drug Development & GxP Intelligence](https://clawhub.com/skills/uplo-pharma) — AI-powered pharmaceutical knowledge management.

## About UPLO

UPLO is the organizational digital twin for AI. Ingest documents, extract structured knowledge, build org context, and expose it via MCP server with GraphRAG. [Learn more](https://uplo.ai)

---

*Built with UPLO — the knowledge layer between your organization and AI.*
