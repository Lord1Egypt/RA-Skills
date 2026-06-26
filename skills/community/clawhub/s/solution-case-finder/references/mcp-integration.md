# MCP Integration

## Confirmed Source

- MCP source name: `triz-solution-search`
- External endpoint pattern observed from the Resource Hub frontend: `https://ai-fabric.patsnap.com/mcp/{source_name}?APP_ID=Patsnap`
- Effective endpoint for this skill: `https://ai-fabric.patsnap.com/mcp/triz-solution-search?APP_ID=Patsnap`

The public endpoint was verified through MCP protocol calls on 2026-06-04.

## Protocol

Use JSON-RPC over HTTP with SSE response support.

Required headers:

```http
Content-Type: application/json
Accept: application/json, text/event-stream
```

Useful verification calls:

```json
{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}
```

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "solution_search",
    "arguments": {
      "user_question": "How can others reduce fan noise without sacrificing airflow in a compact appliance fan design?",
      "limit": 100
    }
  }
}
```

## Tool Schema

Tool name: `solution_search`

Translated tool description:

Given a user's technical problem description, the tool searches a TRIZ-labeled solution case library and returns a ranked list of relevant cases. Each case may include a problem summary, effect summary, innovation summary, TRIZ technical contradiction, SVOP analysis, and scientific effect data.

Input schema:

```json
{
  "type": "object",
  "required": ["user_question"],
  "properties": {
    "limit": {
      "type": "integer",
      "title": "Limit",
      "default": 20,
      "description": "Maximum number of cases to return. Default is 20 and maximum is 100."
    },
    "user_question": {
      "type": "string",
      "title": "User Question",
      "description": "Technical problem description provided by the user"
    }
  }
}
```

Observed response fields:

- `status`
- `error_code`
- `data.total`
- `data.cases[].case_id`
- `data.cases[].problem_summary`
- `data.cases[].effect_summary`
- `data.cases[].innovation_summary`
- `data.cases[].triz_technical_contradiction`
- `data.cases[].triz_svop`
- `data.cases[].triz_scientific_effects`
- `data.cases[].relevance_score`

## Host Configuration

For OpenClaw or Claude Code style clients, add the MCP server by endpoint:

```bash
/mcp add triz-solution-search https://ai-fabric.patsnap.com/mcp/triz-solution-search?APP_ID=Patsnap
```

For clients that need a config object:

```json
{
  "mcpServers": {
    "triz-solution-search": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/inspector",
        "https://ai-fabric.patsnap.com/mcp/triz-solution-search?APP_ID=Patsnap"
      ]
    }
  }
}
```

## Production Note

The Resource Hub frontend marks `APP_ID=Patsnap` as a test value that may be removed. Before public ClawHub release, confirm whether to keep this APP_ID or replace it with a production app id or gateway authentication method.
