# Zoho Social MCP

Connect your agent to Zoho Social through the Model Context Protocol (MCP). This skill provides everything you need to list portals, brands, and channels, inspect drafts and schedules, upload media, and query the Social action catalog using `mcporter`.

This repository contains the public source for the ClawHub skill [`@sprintcx/zoho-social-mcp`](https://clawhub.ai/sprintcx/skills/zoho-social-mcp).

## What This Skill Includes

- Agent Skill instructions in `SKILL.md` (portable SKILL.md format)
- ClawHub release card metadata in `skill-card.md`
- Ready-to-use Python helpers for portals, brands, channels, drafts, schedules, published posts, media listing, and image upload
- A JSON Action catalog with four least-privilege profiles: **social-viewer**, **social-creator**, **social-publisher**, and **social-admin**
- Security-conscious `mcporter` calls through `subprocess.run([...])` without shell expansion
- Explicit pairing with [zoho-attachment-bridge](https://github.com/sprintberlin/zoho-attachment-bridge) for Zoho apps whose MCP upload tools drop binary parameters
- Issue-first contribution rules in [CONTRIBUTING.md](CONTRIBUTING.md). Use native `git` and `gh`; do not add a GitHub wrapper script

## Requirements

| Requirement | Details |
|---|---|
| Zoho Social MCP Server | A configured endpoint from [mcp.zoho.eu](https://mcp.zoho.eu) |
| mcporter | MCP client CLI (bundled with OpenClaw; elsewhere `npm i -g mcporter`) |
| Endpoint selection | `ZOHO_SOCIAL_MCP_URL` for one account; named profiles or `--mcp-url` for multiple accounts |
| Image uploads | `scripts/upload_media.py` encodes a complete data-URI payload. Keep [zoho-attachment-bridge](https://github.com/sprintberlin/zoho-attachment-bridge) linked if a live upload later proves to drop bytes |

### Single-account setup

For the common single-account case, set `ZOHO_SOCIAL_MCP_URL`. The helper scripts also support named profiles and one-off URL overrides.

```bash
export ZOHO_SOCIAL_MCP_URL="https://your-org-zoho-social-xxxxx.zohomcp.eu/mcp/YOUR_TOKEN/message"
```

To verify that it is set without printing the credential:

```bash
if [ -n "$ZOHO_SOCIAL_MCP_URL" ]; then echo "ZOHO_SOCIAL_MCP_URL is set"; else echo "ZOHO_SOCIAL_MCP_URL is not set"; fi
```

Treat `ZOHO_SOCIAL_MCP_URL` like a password. It contains Social access credentials.

## How to Get Your MCP URL

1. Go to [mcp.zoho.eu](https://mcp.zoho.eu) and sign in with your Zoho account.
2. Click **Add Connection** or **New Connection**.
3. Select **Zoho Social** from the list of available apps.
4. Choose the data center matching your Zoho account: EU, US, IN, AU, JP, or CN.
5. Grant the requested OAuth scopes. Enable only the Actions from the profile you intend to use.
6. After authorization, copy the generated MCP endpoint URL.
7. Set it as `ZOHO_SOCIAL_MCP_URL`.

### Multiple organizations and customer accounts

Use one shared profile file instead of changing global environment variables:

```json
{
  "version": 1,
  "profiles": {
    "acme": {
      "services": {
        "social": {"env": "ACME_SOCIAL_MCP_URL"}
      }
    }
  }
}
```

```bash
python3 scripts/list_portals.py --profile acme
```

The default file is `~/.config/zoho-mcp/profiles.json`. Endpoint resolution is `--mcp-url`, selected profile, then the app environment variable. Prefer profile entries using `env` or `url_file`; direct URLs in JSON are supported but make the file credential-bearing. Full format: [`references/MULTI_ACCOUNT.md`](references/MULTI_ACCOUNT.md).

## Quick Start

### List available tools on your MCP server

```bash
mcporter list "$ZOHO_SOCIAL_MCP_URL"
```

### List portals

```bash
cat << 'EOF' > /tmp/social_portals.json
{"headers": {}}
EOF
mcporter call "$ZOHO_SOCIAL_MCP_URL.ZohoSocial_getSocialPortals" --args "$(< /tmp/social_portals.json)"
```

An empty portal list or `USER_INACTIVE_IN_PORTAL` means the authenticated user has no Social workspace access. Do not guess IDs and do not switch to another account.

## Python Scripts

Ready-to-use scripts for common Social operations. They accept `--profile`, `--profiles-file`, and `--mcp-url`, with `ZOHO_SOCIAL_MCP_URL` as the single-account fallback.

The bundled Python scripts call `mcporter` directly through `subprocess.run([...])` and do not invoke a shell.

```bash
python3 scripts/list_portals.py
python3 scripts/list_brands.py --portal-id 123 --json
python3 scripts/list_channels.py --portal-id 123 --brand-id 456
python3 scripts/list_drafts.py --portal-id 123 --brand-id 456 --limit 20
python3 scripts/list_schedules.py --portal-id 123 --brand-id 456
python3 scripts/list_published.py --portal-id 123 --brand-id 456 --network linkedin
python3 scripts/inspect_post.py 789 --kind draft --portal-id 123 --brand-id 456
python3 scripts/list_media.py --portal-id 123 --brand-id 456
python3 scripts/upload_media.py --portal-id 123 --brand-id 456 --file ./hero.png
```

Every helper accepts `--json` and `--timeout`. Run any helper with `--help` without configuring credentials. Unknown or incomplete options exit with status 2.

## Media uploads

Zoho Social currently documents 31 MCP tools. Live `uploadSocialMedia` does **not** use a dropped `format: binary` parameter. It requires a JSON body:

- `file`: complete `data:image/png;base64,<COMPLETE_PAYLOAD>`
- `file_name`: stored filename
- headers `portal_id` and `brand_id`

`uploadSocialMediaFromUrl` fetches a remote image by URL.

Do not paste base64 into chat. `scripts/upload_media.py --file` reads the local bytes and sends the complete data URI. Live `uploadSocialMedia` returns the usable ID in `file_path`. Treat empty `file_path` as failure even when `status` is `success`, then re-list the library with `list_media.py`. Degenerate images can report success and still never appear.

The companion [zoho-attachment-bridge](https://github.com/sprintberlin/zoho-attachment-bridge) remains required for Books, CRM, Projects, and WorkDrive, where MCP upload tools silently drop bytes. Social image uploads go through this skill. A live 400x400 PNG landed in the library with SHA-256 matching the source bytes. Do not extend the bridge for Social unless a later live upload reports success with empty `file_path` and no library asset.

## Social Action Catalog and Profiles

Zoho Social currently exposes 31 MCP Actions. A single Zoho MCP server accepts at most **300 selected Actions**, so the full catalog fits, but enabling everything still inflates the session tool catalog and includes schedule deletion.

| Profile | Actions | Fits the 300 limit |
|---|---|---|
| `social-viewer` | 16 | yes |
| `social-creator` (inherits `social-viewer`) | 23 | yes |
| `social-publisher` (inherits `social-creator`) | 30 | yes |
| `social-admin` (inherits `social-publisher`) | 31 | yes |

The catalog is JSON, not prose:

- [`references/actions.jsonl`](references/actions.jsonl)
- [`references/profiles.json`](references/profiles.json)
- [`references/CATALOG_FORMAT.md`](references/CATALOG_FORMAT.md)
- [`references/ACTION_PROFILES.md`](references/ACTION_PROFILES.md)
- [`references/COMMON_WORKFLOWS.md`](references/COMMON_WORKFLOWS.md)

```bash
python3 scripts/lookup_actions.py --profiles
python3 scripts/lookup_actions.py --profile social-viewer --names-only
python3 scripts/lookup_actions.py --task media-asset-management --names-only
python3 scripts/lookup_actions.py --search "draft"
python3 scripts/lookup_actions.py --action uploadSocialMedia
python3 scripts/lookup_actions.py --validate
```

The four roles:

1. **Social Viewer** (`social-viewer`, 16): read-only portals, brands, channels, drafts, schedules, published posts, media library, mentions, and counts.
2. **Social Creator** (`social-creator`, 23 resolved): drafts, validation, media upload, Pinterest board create, activity comments. No live publish and no schedule mutation.
3. **Social Publisher** (`social-publisher`, 30 resolved): schedule, publish, approval status, draft deletion. No schedule deletion.
4. **Social Administrator** (`social-admin`, 31 resolved): full documented Social MCP surface, including `deleteSocialSchedule`.

After configuring the connection at [mcp.zoho.eu](https://mcp.zoho.eu), verify the actual result:

```bash
mcporter list "$ZOHO_SOCIAL_MCP_URL"
```

Runtime tool names normally add the `ZohoSocial_` prefix.

## Token Optimization (Large MCP Catalogs)

Connecting large MCP servers to OpenClaw can cost a large number of input tokens per session if all tool schemas are loaded eagerly up front.

To avoid loading schemas on session start, enable OpenClaw's built-in Tool Search in `~/.openclaw/openclaw.json`:

```json5
{
  tools: {
    toolSearch: {
      mode: "directory"
    }
  }
}
```

## Troubleshooting

### No endpoint configured

Set `ZOHO_SOCIAL_MCP_URL`, use `--profile`, or pass `--mcp-url`. See [Multi-account profiles](references/MULTI_ACCOUNT.md).

### Empty portals or `USER_INACTIVE_IN_PORTAL`

The authenticated user cannot see a Social workspace. Stop. Do not invent portal or brand IDs and do not switch to another customer's endpoint.

### `Invalid oauth scope to access this URL`

The MCP connection token may have expired or may not include the required scope. Go to [mcp.zoho.eu](https://mcp.zoho.eu), revoke and reconnect the affected app.

### Upload reported success but empty `file_path`

Treat it as failure. Live uploads put the usable ID in `file_path`, not `id`. Re-list the media library. File a GitHub issue with sanitized evidence. Do not add a GitHub wrapper script.

## Repository Files

- `SKILL.md`: Agent Skill instructions.
- `CONTRIBUTING.md`: issue-first native `gh` workflow.
- `references/ACTION_PROFILES.md`: least-privilege Social Action profiles.
- `references/COMMON_WORKFLOWS.md`: verified workflows.
- `references/actions.jsonl`: complete catalog of 31 known Social Actions.
- `references/MULTI_ACCOUNT.md`: portable endpoint profiles.
- `scripts/`: portal, brand, channel, draft, schedule, published, media, and upload helpers.
- `tests/`: credential-free helper and resolver tests.

## Security Notes

The bundled scripts call `mcporter` directly through `subprocess.run([...])` without shell expansion. Social content is customer-facing. Load only required records and never copy contents into chats, logs, or repositories.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

## Publish

Publish under the SprintCX ClawHub organization:

```bash
clawhub skill publish . \
  --slug zoho-social-mcp \
  --name "Zoho Social MCP" \
  --owner sprintcx \
  --version 1.0.0 \
  --source-repo sprintberlin/openclaw-zoho-social-mcp-skill \
  --source-ref main \
  --source-path . \
  --changelog "Initial public Social MCP skill with portable account profiles"
```
