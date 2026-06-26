# Surprise Buddy Skill

Agent skill for the **[Surprise Buddy](https://www.surprise-buddy.com)** gift-search MCP server.

This repository contains the canonical `SKILL.md` for AI agents (Claude, ChatGPT, custom SDK apps) to discover and use Surprise Buddy's curated gift database. It is loaded by Claude Code via `/install` and by other agent frameworks that follow the [Skill format](https://github.com/anthropics/skills) convention.

## What is Surprise Buddy?

Surprise Buddy is a curated, country-scoped gift database exposed via a public Model Context Protocol (MCP) server. International coverage — every result is a real product page on a real marketplace (Amazon, Etsy, Mercado Libre, Otto, Bol.com, Allegro, Jochen Schweizer) and the link can be presented to the user as-is.

**Live MCP endpoint:** `https://www.surprise-buddy.com/api/mcp`

## Files

| File | Purpose |
|---|---|
| [`SKILL.md`](SKILL.md) | The canonical skill definition — tools, parameters, usage instructions for AI agents. |
| [`LICENSE`](LICENSE) | MIT license. |

## Quickstart for agent developers

### Claude Desktop / Claude.ai
```json
{
  "mcpServers": {
    "surprise-buddy": {
      "url": "https://www.surprise-buddy.com/api/mcp"
    }
  }
}
```

### ChatGPT Custom GPT
Import the OpenAPI 3.1 spec as a Custom GPT Action:
```
https://www.surprise-buddy.com/openapi.yaml
```

### Plain HTTP / curl
```bash
curl -X POST https://www.surprise-buddy.com/api/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "find_gifts",
      "arguments": {
        "country": "DE",
        "occasion": "birthday",
        "age": 31,
        "gender": "female",
        "limit": 5
      }
    }
  }'
```

## Exposed tools

- **`find_gifts`** — main search (country required, all other filters optional)
- `list_supported_countries`
- `list_supported_occasions(country?)`
- `list_supported_interests`
- `list_supported_colors`

See [`SKILL.md`](SKILL.md) for the full parameter and response schema.

## Discovery resources

- MCP discovery manifest: <https://www.surprise-buddy.com/.well-known/mcp.json>
- OpenAPI 3.1 spec: <https://www.surprise-buddy.com/openapi.yaml>
- LLMs.txt: <https://www.surprise-buddy.com/llms.txt>
- Developer landing page: <https://www.surprise-buddy.com/en/agents>

## Authentication

None — the MCP server is fully open. Reasonable rate limiting may apply.

## License

[MIT](LICENSE) © Surprise Buddy
