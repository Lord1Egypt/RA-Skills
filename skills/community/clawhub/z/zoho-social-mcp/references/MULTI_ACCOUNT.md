# Multi-account endpoint profiles

The helper CLIs support one simple default endpoint and any number of named Zoho accounts. This is runtime-neutral and works anywhere Python and `mcporter` are available, including OpenClaw and Hermes.

## Resolution order

The MCP endpoint is selected in this order:

1. `--mcp-url URL`
2. `--profile NAME`
3. app-specific or generic profile environment variable
4. app-specific endpoint environment variable

Profile selection uses `--profile`, then `ZOHO_SOCIAL_MCP_PROFILE`, then `ZOHO_MCP_PROFILE`. The profile file uses `--profiles-file`, then `ZOHO_MCP_PROFILES_FILE`, then `~/.config/zoho-mcp/profiles.json`.

Endpoint environment variables:

- CRM: `ZOHO_CRM_MCP_URL`, then legacy `ZOHO_MCP_URL`
- People: `ZOHO_PEOPLE_MCP_URL`
- Books: `ZOHO_BOOKS_MCP_URL`
- Desk: `ZOHO_DESK_MCP_URL`
- WorkDrive: `ZOHO_WORKDRIVE_MCP_URL`
- Social: `ZOHO_SOCIAL_MCP_URL`

## Profile file

Create `~/.config/zoho-mcp/profiles.json`:

```json
{
  "version": 1,
  "profiles": {
    "acme": {
      "services": {
        "crm": {"env": "ACME_CRM_MCP_URL"},
        "people": {"env": "ACME_PEOPLE_MCP_URL"},
        "books": {
          "env": "ACME_BOOKS_MCP_URL",
          "organization_id": "123456789"
        },
        "desk": {"env": "ACME_DESK_MCP_URL"},
        "workdrive": {"env": "ACME_WORKDRIVE_MCP_URL"},
        "social": {"env": "ACME_SOCIAL_MCP_URL"}
      }
    },
    "acme-subsidiary": {
      "services": {
        "social": {"url_file": "secrets/acme-subsidiary-social.url"}
      }
    }
  }
}
```

Each service must define exactly one endpoint source:

- `env`: read the URL from the named environment variable. Recommended when a secret manager injects environment variables.
- `url_file`: read the URL from a local file. Relative paths are resolved from the profile file's directory.
- `url`: store the endpoint directly in the JSON file. Supported for small local installations, but the file then contains a credential.

Lock down local files and never commit them:

```bash
chmod 700 ~/.config/zoho-mcp
chmod 600 ~/.config/zoho-mcp/profiles.json
```

## Usage

```bash
# Single account: no profile needed
export ZOHO_SOCIAL_MCP_URL="https://your-org-zoho-social.example/mcp/YOUR_TOKEN/message"
python3 scripts/list_portals.py

# Named account
python3 scripts/list_portals.py --profile acme

# Select a profile for every compatible helper in one process
export ZOHO_MCP_PROFILE=acme
python3 scripts/list_portals.py

# One-off override
python3 scripts/list_portals.py --mcp-url "https://your-org-zoho-social.example/mcp/YOUR_TOKEN/message"
```

Avoid `--mcp-url` on shared systems because command-line arguments can appear in shell history and process listings. Prefer an injected environment variable, `env`, or `url_file`.

## Agent routing rule

When a task names a customer, subsidiary, or organization, select the matching profile explicitly. Never fall back to another account after an authentication, scope, or lookup error. Before writes, verify the target account with a harmless read or live tool discovery.

An empty portal list or `USER_INACTIVE_IN_PORTAL` means the authenticated user cannot see that Social workspace. Do not guess portal or brand IDs and do not switch to another customer's MCP endpoint.
