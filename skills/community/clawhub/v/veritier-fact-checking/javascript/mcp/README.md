# Veritier - MCP Integration (JavaScript)

JavaScript clients talk to Veritier over remote Streamable HTTP, with no local proxy in the way. The stdio proxy is Python-only and lives in [`python/mcp/`](../../python/mcp/).

📦 **API Docs:** [veritier.ai/docs](https://veritier.ai/docs#mcp) · 📐 **OpenAPI:** [api.veritier.ai/openapi.json](https://api.veritier.ai/openapi.json)

---

## Remote HTTP

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
cd javascript
npm install
node mcp/mcp_test.mjs
```

Expected tools: `extract_text`, `extract_document`, `verify_text`, `verify_document`, `validate`, `attest_action`.

Given a `vt_test_` key, the script goes further and calls `attest_action` with `mock_decision=allow` and `verify_text` with an `action_id`.

MCP tools always answer synchronously. Reconstructing a Claim Credential is a REST call:

`GET https://api.veritier.ai/v1/credentials/{id}`

---

## Tools

| Tool | Description |
|------|-------------|
| `extract_text` / `extract_document` | Pulls out the checkable claims without verifying them |
| `verify_text` / `verify_document` | Fact-checks each claim. An optional `action_id` mints an informational credential |
| `validate` | Authenticity scan. The parameter is `url` on MCP and `document_url` on REST |
| `attest_action` | Returns `allow`, `block`, or `escalate`, all with HTTP 200. A `block` means the agent must not run the call. MCP is text-only; `procedure` defaults to `package_exists`; `policy_ground` uses `reference_text` (MCP-only alias). REST is a different schema — see [SKILL.md](../../SKILL.md). |

---

## Need help?

- **Skill file:** [SKILL.md](../../SKILL.md)
- **Python stdio proxy:** [`python/mcp/`](../../python/mcp/)
