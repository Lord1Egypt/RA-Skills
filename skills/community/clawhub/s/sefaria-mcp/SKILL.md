---
name: sefaria-mcp
openclaw:
  requires:
    node: ">=18"
  install:
    - id: node
      kind: node
      package: sefaria-mcp-server
      bins:
        - sefaria-mcp
---

# Sefaria MCP Server

An MCP (Model Context Protocol) server that provides access to [Sefaria](https://www.sefaria.org)'s library of Jewish texts — Torah, Talmud, Mishnah, Midrash, and thousands of commentaries.

## Tools

| Tool | Description |
|------|-------------|
| `get_text` | Read any text by reference (Genesis 1:1, Berakhot 2a, Rashi on Exodus 3:14, etc.) |
| `search` | Full-text search across all texts in English or Hebrew |
| `get_links` | Get commentaries and cross-references for a verse |
| `get_parsha` | Get this week's Torah portion |
| `get_calendars` | Get today's learning schedule (Daf Yomi, Parsha, daily Rambam, etc.) |
| `get_book_info` | Get metadata about a book (structure, categories) |
| `get_related` | Get related topics and community source sheets |

## Usage

```json
{
  "mcpServers": {
    "sefaria": {
      "command": "npx",
      "args": ["-y", "sefaria-mcp-server"]
    }
  }
}
```

## Configuration

No API key required — Sefaria's public API is free and open.

## Links

- npm: https://www.npmjs.com/package/sefaria-mcp-server
- GitHub: https://github.com/abeperl/sefaria-mcp-server
- Sefaria: https://www.sefaria.org
