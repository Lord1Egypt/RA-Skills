# Veritier - MCP Integration (JavaScript)

Connect any MCP-compatible AI agent to Veritier's real-time fact-checking engine from JavaScript. The **Model Context Protocol (MCP)** is an open standard that lets AI agents discover and use external tools - Veritier exposes four tools for claim extraction and verification.

📦 **API Docs:** [veritier.ai/docs](https://veritier.ai/docs) · 🔑 **Get your free key:** [veritier.ai/register](https://veritier.ai/register)

---

## Remote HTTP (recommended - zero install)

Point your MCP client directly at the Veritier cloud endpoint. No local proxy, no setup.

```json
{
  "mcpServers": {
    "veritier": {
      "type": "http",
      "url": "https://api.veritier.ai/mcp/",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

Or via MCP CLI:

```bash
mcp add --transport http veritier https://api.veritier.ai/mcp/ \
  --header "Authorization: Bearer YOUR_API_KEY"
```

---

## Verify Your Integration

Run the included test script to confirm everything works:

```bash
cd javascript
npm install
node mcp/mcp_test.mjs
```

Expected output:

```
✓ Initialize: server=veritier v2.1.1
✓ Tools discovered: [extract_text, extract_document, verify_text, verify_document]
✓ extract_text result:
  - The Eiffel Tower is located in Paris, France.
  - The Eiffel Tower stands 330 metres tall.
✓ verify_text result:
  Claim: 'The Eiffel Tower is located in Berlin.'
    Verdict: False
    ...
✓ All checks passed! Your MCP integration is working correctly.
```

---

## Available Tools

Once connected, your agent has access to:

| Tool | Description | Quota |
|------|-------------|-------|
| `extract_text` | Extract falsifiable claims from raw text | Extractions |
| `extract_document` | Extract claims from a URL document | Extractions |
| `verify_text` | Extract + fact-check claims from raw text | Verifications |
| `verify_document` | Extract + fact-check claims from a URL document | Verifications |

---

## Files in This Folder

| File | Description |
|------|-------------|
| [mcp_test.mjs](mcp_test.mjs) | Integration test - verifies MCP connectivity using native `fetch` |

> **Note:** For a local stdio proxy (required by some MCP clients), see the [Python MCP folder](../../python/mcp/). The stdio proxy is Python-only because the `mcp` SDK used for stdio transport is a Python package.

---

## Need Help?

- **Full docs:** [veritier.ai/docs](https://veritier.ai/docs)
- **Python MCP proxy:** See [`python/mcp/`](../../python/mcp/) for the local stdio proxy
- **JavaScript examples:** See the parent [`javascript/`](../) folder
- **Agent skill file:** See [SKILL.md](../../SKILL.md) at the repository root
