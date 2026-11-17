# VMEG MCP Common Configuration (All Platforms)

Skill install paths and MCP config file locations are in each platform's `setup-{platform}.md`.  
**Do not hardcode MCP UI shortcuts in this Skill** — search "MCP" in Command Palette / Settings, or read the platform's official docs.

## Endpoint

| Item | Value |
|------|-------|
| MCP URL | `https://www.vmeg.ai/api/mcp` |
| Sign-in | `https://www.vmeg.ai/signin` |

## Authentication (choose one, do not mix)

See [oauth.md](oauth.md).

| | OAuth | API Key (`vmeg_sk_`) |
|---|--------|----------------------|
| Config | URL only | URL + `Authorization: Bearer vmeg_sk_xxx` |
| Connect | **Connect** in MCP UI → browser login → **select project** | No Connect needed |
| Get key | — | [VMEG console](https://www.vmeg.ai) → Settings → API Key |

### OAuth config example (most agents)

```json
{
  "mcpServers": {
    "vmeg": {
      "url": "https://www.vmeg.ai/api/mcp"
    }
  }
}
```

### API Key config example

```json
{
  "mcpServers": {
    "vmeg": {
      "url": "https://www.vmeg.ai/api/mcp",
      "headers": {
        "Authorization": "Bearer vmeg_sk_YOUR_KEY"
      }
    }
  }
}
```

After saving: confirm `vmeg` is connected in MCP UI; OAuth requires Connect.  
More examples: [assets/mcp-config-examples/](../assets/mcp-config-examples/)

## Verify

In Agent, say: "List my VMEG materials" → should call `vmeg_list_materials`.

## Local file upload

**OAuth recommended (presigned; curl needs no VMEG Bearer):**

1. Compute file MD5 → `vmeg_initiate_material_upload`
2. `curl -X PUT --upload-file @/path/to/file.ext "<presignedPutUrl>"`
3. `vmeg_complete_material_upload` → get `materialId`

**API Key alternative:** `POST /api/mcp/material/upload` (multipart + Bearer). See [oauth.md](oauth.md).

Business details follow **MCP server instructions** after connecting.

## Troubleshooting (VMEG side)

| Symptom | Fix |
|---------|-----|
| Authentication required | Re-Connect OAuth, or check API Key |
| 401 from mixing OAuth + API Key | Remove extra Header; use one method only |
| No tools after login | Confirm **project selected** at login; restart agent |
| Client has no Connect | Use API Key instead |
| Skill installed but no tool calls | Confirm MCP connected; use Agent mode |

Platform-specific MCP logs: check official docs; do not rely on hardcoded shortcuts in this Skill.
