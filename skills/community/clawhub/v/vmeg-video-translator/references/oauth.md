# VMEG MCP Authentication

VMEG Remote MCP supports **OAuth** and **API Key** — **choose one**, do not mix.

Common config and verification: [setup-common.md](setup-common.md)

## Endpoints

| Item | URL |
|------|-----|
| MCP | `https://www.vmeg.ai/api/mcp` |
| Sign-in | `https://www.vmeg.ai/signin` |

## Which to use

| | OAuth (recommended for individuals) | API Key (`vmeg_sk_`) |
|---|--------------------------------------|----------------------|
| Best for | Daily use in Cursor, Claude Code, etc. | Fixed secret, or when OAuth Connect is unavailable |
| MCP config | URL only; **Connect** in MCP UI | URL + `Authorization: Bearer vmeg_sk_xxx` |
| Project | **Select project** in browser at login | Bound when key was created |

## OAuth workflow

1. Put URL only in MCP config (format in platform `setup-*.md` and [setup-common.md](setup-common.md))
2. Open MCP UI in **current agent** (search "MCP" in Command Palette / Settings)
3. Find `vmeg`, click **Connect**
4. Browser → VMEG login → **select project**
5. Back in agent: confirm `vmeg` connected and `vmeg_*` tools visible

**Do not** add API Key Header in OAuth mode.

## Get API Key

1. Open [VMEG console](https://www.vmeg.ai) and sign in
2. Go to **Settings → API Key**
3. Create key, copy `vmeg_sk_...` (shown once — save it)

Add Header in MCP config (example in [setup-common.md](setup-common.md)).

## Local material upload

### OAuth recommended: presigned two-step (curl needs no VMEG Bearer)

1. `vmeg_initiate_material_upload` (`fileHash` + `extName`)
2. `curl -X PUT --upload-file @/path/to/file.ext "<presignedPutUrl>"`
3. `vmeg_complete_material_upload` → `materialId`

### API Key alternative: one-step multipart

`POST https://www.vmeg.ai/api/mcp/material/upload`, `Authorization: Bearer vmeg_sk_...`, field `file`.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Login required / Authentication required | Re-**Connect** OAuth, or verify API Key |
| Connected but tools 401 | Do **not** mix OAuth + API Key; remove extra Header |
| No tools after login | Confirm **project selected**; restart agent |
| No Connect button | Use API Key instead |
| Where is MCP settings? | Search "MCP" or read official docs |

Config examples: [assets/mcp-config-examples/](../assets/mcp-config-examples/)
