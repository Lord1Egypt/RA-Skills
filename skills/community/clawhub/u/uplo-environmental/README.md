# UPLO Environmental — Impact & Compliance Intelligence

AI-powered environmental knowledge management. Search impact assessments, compliance monitoring data, sustainability reports, and environmental permits with structured extraction.

[![ClawHub](https://img.shields.io/badge/ClawHub-uplo-environmental-blue)](https://clawhub.com/skills/uplo-environmental)
[![MCP](https://img.shields.io/badge/MCP-21_tools-green)](https://uplo.ai)
[![Schemas](https://img.shields.io/badge/schemas-4-orange)](https://uplo.ai/schemas)

## Quick Install

```bash
clawhub install uplo-environmental
```

Or add to your Claude Desktop config:

```json
{
  "mcpServers": {
    "uplo-environmental": {
      "command": "npx",
      "args": ["-y", "@agentdocs1/mcp-server", "--http"],
      "env": {
        "AGENTDOCS_URL": "https://your-instance.uplo.ai",
        "API_KEY": "your-api-key",
        "DEFAULT_PACKS": "environmental"
      }
    }
  }
}
```

## What You Get

- **4 industry schemas** — pre-built extraction templates for Environmental documents
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

- **Environmental** — 4 schemas

## Related Skills

- [UPLO Sustainability — ESG & Environmental Intelligence](https://clawhub.com/skills/uplo-sustainability) — AI-powered sustainability intelligence spanning environmental, energy, and agriculture.
- [UPLO Agriculture — Crop & Compliance Intelligence](https://clawhub.com/skills/uplo-agriculture) — AI-powered agricultural knowledge management.
- [UPLO Compliance — Cross-Domain Regulatory Intelligence](https://clawhub.com/skills/uplo-compliance) — AI-powered compliance intelligence spanning legal, financial, and government regulatory requirements.

## About UPLO

UPLO is the organizational digital twin for AI. Ingest documents, extract structured knowledge, build org context, and expose it via MCP server with GraphRAG. [Learn more](https://uplo.ai)

---

*Built with UPLO — the knowledge layer between your organization and AI.*
