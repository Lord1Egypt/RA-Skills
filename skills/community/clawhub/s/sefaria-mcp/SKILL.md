# Sefaria MCP Server

Access Jewish texts (Torah, Talmud, Mishnah, Midrash, Commentaries) via MCP.

## Installation

```bash
npm install -g sefaria-mcp-server
```

Or run directly:

```bash
npx sefaria-mcp-server
```

## Configuration

Add to your MCP config:

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

## Tools

| Tool | Description |
|------|-------------|
| `get_text` | Get text by reference (Genesis 1:1, Berakhot 2a, etc.) |
| `search` | Full-text search across all texts |
| `get_links` | Get commentaries and cross-references |
| `get_parsha` | Get this week's Torah portion |
| `get_calendars` | Daily learning (Daf Yomi, Rambam, etc.) |
| `get_book_info` | Book metadata and structure |
| `get_related` | Related topics and source sheets |

## Examples

- "What does Genesis 1:1 say? Show me the Hebrew and commentaries."
- "Search for texts about loving your neighbor"
- "What's this week's parsha?"
- "What's today's Daf Yomi?"

## Credits

- Powered by [Sefaria](https://www.sefaria.org)
- npm: [sefaria-mcp-server](https://www.npmjs.com/package/sefaria-mcp-server)
- GitHub: [abeperl/sefaria-mcp-server](https://github.com/abeperl/sefaria-mcp-server)
