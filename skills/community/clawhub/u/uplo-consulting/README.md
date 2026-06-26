# UPLO Consulting — Engagement & Methodology Intelligence

AI-powered consulting knowledge management. Search engagement records, methodology frameworks, deliverable templates, and best practices with structured extraction.

[![ClawHub](https://img.shields.io/badge/ClawHub-uplo-consulting-blue)](https://clawhub.com/skills/uplo-consulting)
[![MCP](https://img.shields.io/badge/MCP-21_tools-green)](https://uplo.ai)
[![Schemas](https://img.shields.io/badge/schemas-4-orange)](https://uplo.ai/schemas)

## Quick Install

```bash
clawhub install uplo-consulting
```

Or add to your Claude Desktop config:

```json
{
  "mcpServers": {
    "uplo-consulting": {
      "command": "npx",
      "args": ["-y", "@agentdocs1/mcp-server", "--http"],
      "env": {
        "AGENTDOCS_URL": "https://your-instance.uplo.ai",
        "API_KEY": "your-api-key",
        "DEFAULT_PACKS": "consulting"
      }
    }
  }
}
```

## What You Get

- **4 industry schemas** — pre-built extraction templates for Consulting documents
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

- **Consulting** — 4 schemas

## Related Skills

- [UPLO Professional Services — Engagement & Knowledge Intelligence](https://clawhub.com/skills/uplo-professional-services) — AI-powered professional services intelligence spanning consulting, accounting, architecture, and research.
- [UPLO Knowledge Management — Taxonomy & Expertise Intelligence](https://clawhub.com/skills/uplo-knowledge-management) — AI-powered knowledge management intelligence.
- [UPLO Accounting — Bookkeeping & Tax Intelligence](https://clawhub.com/skills/uplo-accounting) — AI-powered accounting knowledge management.

## About UPLO

UPLO is the organizational digital twin for AI. Ingest documents, extract structured knowledge, build org context, and expose it via MCP server with GraphRAG. [Learn more](https://uplo.ai)

---

*Built with UPLO — the knowledge layer between your organization and AI.*
