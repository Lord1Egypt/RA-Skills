# Veritier - MCP Integration

Connect any MCP-compatible AI agent to Veritier's real-time fact-checking engine. The **Model Context Protocol (MCP)** is an open standard that lets AI agents discover and use external tools - Veritier exposes four tools for claim extraction and verification.

📦 **API Docs:** [veritier.ai/docs](https://veritier.ai/docs) · 🔑 **Get your free key:** [veritier.ai/register](https://veritier.ai/register)

---

## Option A: Remote HTTP (recommended - zero install)

Point your MCP client directly at the Veritier cloud endpoint. No Python, no proxy, no local setup.

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

## Option B: Local stdio Proxy

For MCP clients that require a local subprocess (stdio transport) instead of a remote HTTP connection.

### Prerequisites

- Python 3.10+
- `pip install mcp httpx anyio`

### Setup

**1. Set your API key:**

```bash
# macOS / Linux
export VERITIER_API_KEY="vt_your_key_here"

# Windows (PowerShell)
$env:VERITIER_API_KEY = "vt_your_key_here"
```

**2. Configure your MCP client:**

```json
{
  "mcpServers": {
    "veritier": {
      "command": "python",
      "args": ["/absolute/path/to/mcp/veritier_mcp_proxy.py"],
      "env": {
        "VERITIER_API_KEY": "vt_your_key_here"
      }
    }
  }
}
```

**3. Verify it works:**

```bash
python veritier_mcp_test.py
```

Expected output:

```
✓ Initialize: server=veritier-proxy v2.1.1
✓ Tools discovered: ['extract_text', 'extract_document', 'verify_text', 'verify_document']
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

Once connected (via either method), your agent has access to:

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
| [veritier_mcp_proxy.py](veritier_mcp_proxy.py) | Lightweight stdio proxy - bridges local MCP clients to the Veritier API |
| [veritier_mcp_test.py](veritier_mcp_test.py) | Integration test - verifies your proxy setup is working correctly |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `Error: mcp is required` | Run `pip install mcp` |
| `Error: httpx is required` | Run `pip install httpx` |
| `VERITIER_API_KEY not set` | Set the env var or add it to your MCP client's `env` config |
| Timeout errors | Check your internet connection; the API may need up to 120s for large documents |
| `402` response | Monthly quota exhausted - upgrade at [veritier.ai/dashboard](https://veritier.ai/dashboard) |

---

## Need Help?

- **Full docs:** [veritier.ai/docs](https://veritier.ai/docs)
- **Python examples:** See the parent [`python/`](../) folder
- **JavaScript examples:** See the [`javascript/`](../../javascript/) folder
- **Agent skill file:** See [SKILL.md](../../SKILL.md) at the repository root
