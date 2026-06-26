# Reversal — Agent Input Reliability Layer

Normalizes any source (URL, PDF, Word, Excel, CSV, image, dashboard screenshot)
into clean structured JSON in under 2 seconds.

Stop your agents from hallucinating on raw HTML, failing on complex PDFs,
or overflowing their context window on long documents.
One call. Universal schema. Every format. Every time.

## When to use this skill

- Your agent needs to read a URL, article, or webpage without ads/noise
- Your agent needs to parse a PDF, Word doc, or Excel file
- Your agent needs to extract metrics from a dashboard screenshot
- You have multiple sources and want a single normalized schema
- You want deterministic, LLM-ready JSON instead of raw content

## Tools

### reverse_read(source)

Converts any source into structured JSON ready for LLM ingestion.

```
Input:  source  — URL (https://…) or file path (/path/to/file.pdf)
Output: { status, content_type, source, processed_in_ms, data: { title, summary_hint, word_count, content, … } }
```

Supported types: `url` · `pdf` · `word` · `excel` · `csv` · `image` · `text`

### detect_content_type(source)

Lightweight probe — detects content type without full parse.
Use before reverse_read to branch on type.

```
Input:  source  — URL or file path
Output: { source, detected_type }
```

### batch_reverse(sources[])

Normalize up to 10 sources in a single call.
Failed sources return an `error` field without aborting the batch.

```
Input:  sources  — array of 1–10 URLs or file paths
Output: [ { source, result } | { source, error } ]
```

### upload_file(file_path)

Upload a local file; returns a `file_id` for use in reverse_read as `file:<file_id>`.
Validates extension before write. Supported: pdf, docx, xlsx, xls, csv, png, jpg, jpeg, webp, gif, txt, md.

```
Input:  file_path  — absolute path to local file
Output: { file_id, filename, size_bytes }
```

## Install — stdio (local agents)

Works with Claude Desktop, Cursor, Windsurf, and any stdio MCP host.

```bash
git clone https://github.com/Etytabs/REVERSAL
cd REVERSAL
pip install -r requirements.txt
pip install -e .
```

Add to your MCP config:

```json
{
  "mcpServers": {
    "reversal": {
      "command": "python",
      "args": ["-m", "reversal_engine.mcp_server"],
      "cwd": "/path/to/REVERSAL"
    }
  }
}
```

No API key required for URL, PDF, Word, Excel, CSV, and text parsing.
Set `ANTHROPIC_API_KEY` only if you need image/dashboard screenshot parsing.

## Install — HTTP (remote agents)

Works with OpenAI Codex, Claude Web, and any MCP-over-HTTP host.

```bash
# 1. Get a free API key
curl -X POST https://api.reversal.dev/v1/register \
  -H "Content-Type: application/json" \
  -d '{"email": "you@example.com"}'
# → { "api_key": "sk-rev-…" }
```

```json
{
  "mcpServers": {
    "reversal": {
      "transport": "http",
      "url": "https://api.reversal.dev/v1/mcp",
      "headers": { "Authorization": "Bearer sk-rev-YOUR_KEY" }
    }
  }
}
```

For OpenAI Codex (`~/.codex/config.toml`):

```toml
[[mcp_servers]]
name = "reversal"
url  = "https://api.reversal.dev/v1/mcp"
[mcp_servers.headers]
Authorization = "Bearer sk-rev-YOUR_KEY"
```

## Output schema

Every source returns the same envelope:

```json
{
  "reversal_engine": "1.0",
  "status": "ok",
  "content_type": "url | pdf | word | excel | csv | image | text",
  "source": "original source",
  "processed_in_ms": 142,
  "data": {
    "title": "…",
    "summary_hint": "first 300 chars…",
    "word_count": 1240,
    "content": []
  }
}
```

## Python SDK

```bash
pip install reversal-sdk
```

```python
from reversal_sdk import ReversalClient

client = ReversalClient(api_key="sk-rev-…")

result = client.reverse("https://example.com/report")
print(result["summary"])

# Batch
results = client.batch([
    "https://example.com/report",
    "/path/to/data.xlsx",
])

# LangChain tool
from langchain.tools import tool

@tool
def reversal_tool(source: str) -> str:
    """Normalize any URL or file into structured JSON for the agent."""
    return client.reverse(source)["summary"]
```

## TypeScript SDK

```bash
npm install reversal-client
```

```typescript
import { ReversalClient } from "reversal-client";

const client = new ReversalClient({ apiKey: "sk-rev-…" });

const result = await client.reverse("https://example.com/report");
console.log(result.summary);

// Vercel AI SDK tool
import { tool } from "ai";
import { z } from "zod";

const reversalTool = tool({
  description: "Normalize any URL or file into structured JSON.",
  parameters: z.object({ source: z.string() }),
  execute: async ({ source }) => client.reverse(source),
});
```

## Security

- SSRF protection: all URLs validated against RFC-1918, loopback, link-local, and metadata endpoints
- HMAC-SHA256 signed API keys — default secrets rejected at startup
- JSON-only Redis cache — no pickle, no RCE surface
- File uploads validated by extension allowlist before write
- Optional OTP-gated registration (`REVERSAL_REGISTER_REQUIRE_OTP=true`)
- Per-IP rate limiting on registration (3/min)
- Non-root Docker runtime (uid 1001)
- No obfuscated install commands · No curl|sh · No undeclared secrets

## Repository

https://github.com/Etytabs/REVERSAL
