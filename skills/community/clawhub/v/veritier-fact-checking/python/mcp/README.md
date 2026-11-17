# Veritier - MCP Integration

Connect any MCP-compatible agent to Veritier. The server exposes six tools: claim extraction and fact-checking for both raw text and URLs, an authenticity scan for documents, and `attest_action`, which can stop a tool call before it runs.

📦 **API Docs:** [veritier.ai/docs](https://veritier.ai/docs#mcp) · 🔑 **Get your free key:** [veritier.ai/register](https://veritier.ai/register)

---

## Option A: Remote HTTP (recommended)

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

```bash
mcp add --transport http veritier https://api.veritier.ai/mcp/ \
  --header "Authorization: Bearer YOUR_API_KEY"
```

---

## Option B: Local stdio proxy

For clients that require a local subprocess. Install the dependencies, export your key, and run the test script to confirm the proxy talks to the API:

```bash
pip install mcp httpx anyio
export VERITIER_API_KEY="vt_your_key_here"   # or vt_test_... for zero-quota
python veritier_mcp_test.py
```

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

Expected (test key):

```
✓ Initialize: server=veritier-proxy v2.2.0
✓ Tools discovered: ['extract_text', 'extract_document', 'verify_text', 'verify_document', 'validate', 'attest_action']
```

MCP tools always answer synchronously, so `use_webhook` has no effect here. Reconstructing a credential, fetching the JWKS, and revoking are REST operations rather than MCP tools.

---

## Tools

| Tool | Description | Quota |
|------|-------------|-------|
| `extract_text` | Extract falsifiable claims from raw text | Extractions |
| `extract_document` | Extract claims from a URL document | Extractions |
| `verify_text` | Extract + fact-check. An optional `action_id` mints an informational credential, and does not fail-close | Verifications |
| `verify_document` | Same, for a document at a URL | Verifications |
| `validate` | Authenticity scan. The parameter is named `url` on MCP | Validations |
| `attest_action` | Looks the action up in a system of record and returns a decision plus a signed Claim Credential | Verifications |

`attest_action` picks its system of record from the `procedure` you pass. On MCP, `procedure` defaults to `package_exists` when omitted, input is **text-only**, and `policy_ground` takes `reference_text` (an MCP-only alias the server wraps into a single text `GroundingReference`). REST `POST /v1/attest_action` is a different contract: `procedure` is required, input is `text` XOR `document`, and `policy_ground` uses `grounding_references`. See [openapi.json](https://api.veritier.ai/openapi.json) and [`SKILL.md`](../../SKILL.md).

| Procedure | Checks |
|-----------|--------|
| `package_exists` | The package is published on npm or PyPI |
| `citation_exists` | The case exists in CourtListener, and any quoted passage appears in the matched opinion |
| `filing_exists` | The filing is on SEC EDGAR |
| `statute_exists` | The section exists in the U.S. Code or the Internal Revenue Code, via Cornell LII |
| `policy_ground` | The action is supported by the corpus you supply (`reference_text` on MCP) |

The decision comes back as `allow`, `block`, or `escalate`, and all three arrive with HTTP 200. A `block` means the gate fired and the agent must not run the call.

A key prefixed `vt_test_` runs any of these tools without drawing on your quota. Pass `mock_claims`, `mock_verdict`, `mock_validation`, or `mock_decision` to choose the response you get back.

---

## Files

| File | Description |
|------|-------------|
| [veritier_mcp_proxy.py](veritier_mcp_proxy.py) | The stdio proxy itself, version 2.2 |
| [veritier_mcp_test.py](veritier_mcp_test.py) | Spawns the proxy from this directory and calls every tool |

---

## Need help?

- **Skill file:** [SKILL.md](../../SKILL.md)
- **REST samples:** [python/](../)
- **JavaScript MCP HTTP test:** [javascript/mcp/](../../javascript/mcp/)
