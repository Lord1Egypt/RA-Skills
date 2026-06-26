---
name: onedrive
description: Read, manage, share, upload, and download OneDrive files via Microsoft Graph API. Use when the user asks about OneDrive, OneDrive for Business, SharePoint document libraries, file sharing, or cloud storage on Microsoft.
version: 1.0.0
author: trendex
---

# OneDrive Skill

Access OneDrive (personal + business) and SharePoint document libraries via Microsoft Graph using OAuth2.

## Quick Setup (Automated)

```bash
# Requires: Azure CLI, jq
./scripts/onedrive-setup.sh
```

The setup script will:
1. Log you into Azure (device code flow)
2. Create an App Registration automatically
3. Configure API permissions (Files.ReadWrite.All, Sites.ReadWrite.All, User.Read)
4. Guide you through authorization
5. Save credentials to `~/.onedrive-mcp/`

## Manual Setup

See `references/setup.md` for step-by-step manual configuration via Azure Portal.

## Bootstrap (Headless / Pre-Provisioned Tokens)

If the deployment system already has `client_id`, `client_secret`, `access_token`, and `refresh_token`, run the templated bootstrap script (substituting the `__PLACEHOLDERS__`):

```bash
bash scripts/onedrive-bootstrap.sh
```

It installs `jq` + `curl` if missing, writes `~/.onedrive-mcp/{config,credentials}.json`, refreshes the token, and probes `/me/drive` to confirm. No browser, no Azure CLI.

## Usage

### Token Management
```bash
./scripts/onedrive-token.sh refresh  # Refresh expired token
./scripts/onedrive-token.sh test     # Test connection
./scripts/onedrive-token.sh get      # Print access token
./scripts/onedrive-token.sh info     # Show token info / expiry
./scripts/onedrive-token.sh me       # Show signed-in user
```

### Browsing Files
```bash
./scripts/onedrive-files.sh list                    # List root folder
./scripts/onedrive-files.sh list "Documents"        # List a folder by path
./scripts/onedrive-files.sh list-id <item-id>       # List by item ID
./scripts/onedrive-files.sh list-special documents  # documents|photos|cameraroll|approot|music
./scripts/onedrive-files.sh tree [path] [depth=3]   # Recursive tree
./scripts/onedrive-files.sh recent [count]          # Recently used files
./scripts/onedrive-files.sh shared [count]          # Items shared with me
./scripts/onedrive-files.sh search "<query>" [top]  # Full-text search
```

### Inspecting Items
```bash
./scripts/onedrive-files.sh info <path-or-id>       # Full metadata
./scripts/onedrive-files.sh stat <path-or-id>       # Size, mime, modified
./scripts/onedrive-files.sh url <path-or-id>        # Pre-auth download URL
./scripts/onedrive-files.sh thumbnail <id> [size]   # small | medium | large
./scripts/onedrive-files.sh preview <id>            # Embeddable preview URL
./scripts/onedrive-files.sh versions <id>           # Version history
./scripts/onedrive-files.sh owner <path-or-id>      # Creator / last modifier
```

### Uploading / Downloading
```bash
./scripts/onedrive-files.sh mkdir <path>            # Create folder (parents auto-created)
./scripts/onedrive-files.sh upload <local> <remote> # Auto: simple (≤4MB) or resumable
./scripts/onedrive-files.sh upload-stream <remote>  # Pipe stdin to remote
./scripts/onedrive-files.sh download <remote> [local]
./scripts/onedrive-files.sh cat <path>              # Print text file to stdout
```

### Modifying / Deleting
```bash
./scripts/onedrive-files.sh rename <id-or-path> <new-name>
./scripts/onedrive-files.sh move   <src> <dest-folder>
./scripts/onedrive-files.sh copy   <src> <dest-folder> [new-name]
./scripts/onedrive-files.sh delete <id-or-path>     # → recycle bin
```

### Sharing
```bash
# Anonymous / org-scoped links
./scripts/onedrive-share.sh link <path-or-id> view  anonymous
./scripts/onedrive-share.sh link <path-or-id> edit  anonymous
./scripts/onedrive-share.sh link <path-or-id> view  organization
./scripts/onedrive-share.sh link <path-or-id> embed anonymous
./scripts/onedrive-share.sh link <path-or-id> view  anonymous --password "secret" --expiry 2026-12-31

# Invite specific users
./scripts/onedrive-share.sh invite <path-or-id> alice@example.com read "Have a look!"
./scripts/onedrive-share.sh invite <path-or-id> alice@x.com,bob@y.com write "Please review"

# Permissions
./scripts/onedrive-share.sh permissions <path-or-id>           # List
./scripts/onedrive-share.sh revoke      <path-or-id> <perm-id>
./scripts/onedrive-share.sh update-role <path-or-id> <perm-id> <new-role>

# Resolve a 1drv.ms / SharePoint share URL
./scripts/onedrive-share.sh open "https://1drv.ms/u/s!..."
```

### Drives & Quota
```bash
./scripts/onedrive-files.sh drives           # List drives the user can access
./scripts/onedrive-files.sh drive [drive-id] # Drive metadata (default: yours)
./scripts/onedrive-files.sh quota            # total / used / remaining
./scripts/onedrive-files.sh delta [token]    # Change feed (initial or incremental)
```

### Example Output

```bash
$ ./scripts/onedrive-files.sh list

{
  "kind": "dir",
  "name": "Documents",
  "size": 5242880,
  "modified": "2026-05-15T10:24:31Z",
  "id": "01ABCDEF1234ZZZ",
  "mime": null,
  "children": 12
}
{
  "kind": "file",
  "name": "Budget-Q2.xlsx",
  "size": 184320,
  "modified": "2026-05-18T16:02:11Z",
  "id": "01ABCDEF5678YYY",
  "mime": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
}

$ ./scripts/onedrive-files.sh quota

{
  "state": "normal",
  "total": 1099511627776,
  "used": 482918400,
  "remaining": 1099028709376,
  "deleted": 0
}

$ ./scripts/onedrive-share.sh link "Reports/q1.xlsx" view organization

{
  "id": "aTo...",
  "type": "view",
  "scope": "organization",
  "webUrl": "https://contoso-my.sharepoint.com/:x:/p/...",
  "expirationDateTime": null,
  "hasPassword": false
}

$ ./scripts/onedrive-token.sh me

{
  "id": "9b8...-...-...",
  "displayName": "Jane Doe",
  "userPrincipalName": "jane@contoso.onmicrosoft.com",
  "mail": "jane@contoso.com",
  "givenName": "Jane",
  "surname": "Doe",
  "jobTitle": "Engineer"
}
```

## Token Refresh

Access tokens expire after ~1 hour. Refresh with:

```bash
./scripts/onedrive-token.sh refresh
```

This requires a valid `refresh_token` in the credentials file (kept ~90 days for personal accounts).

## Files

- `~/.onedrive-mcp/config.json` — Client ID, secret, tenant, scopes
- `~/.onedrive-mcp/credentials.json` — OAuth tokens (access + refresh)

Both files are `chmod 600`, directory `700`. Never commit them.

## Permissions

Delegated scopes used by default:

- `Files.ReadWrite.All` — Read/write all files the user can access
- `Sites.ReadWrite.All` — SharePoint / OneDrive for Business document libraries
- `User.Read` — Basic profile (needed for sign-in)
- `offline_access` — Refresh tokens (stay logged in)

See `references/permissions.md` for the full scope catalog (delegated + application/daemon flows).

## Targeting Other Drives

By default, all commands target `/me/drive` (the signed-in user's drive). To target a different drive, set:

```bash
export ONEDRIVE_DRIVE_PREFIX="/drives/<drive-id>"          # Specific drive by ID
export ONEDRIVE_DRIVE_PREFIX="/sites/<site-id>/drive"      # SharePoint site default doc library
export ONEDRIVE_DRIVE_PREFIX="/users/<user-id>/drive"      # Another user (requires Files.Read.All)
```

Discover drive IDs with `./scripts/onedrive-files.sh drives`.

## Bring Your Own Access Token

If you already have a Microsoft Graph access token (from another app / Postman / MSAL / etc.), three options:

```bash
# A) Env var (one-shot)
export ONEDRIVE_ACCESS_TOKEN="eyJ0..."
./scripts/onedrive-files.sh list

# B) Helper (persists to ~/.onedrive-mcp/credentials.json)
./scripts/onedrive-token.sh set "eyJ0..." "refresh-token"

# C) Drop the JSON file directly
mkdir -p ~/.onedrive-mcp && chmod 700 ~/.onedrive-mcp
cat > ~/.onedrive-mcp/credentials.json <<EOF
{"token_type":"Bearer","access_token":"eyJ0...","refresh_token":"..."}
EOF
chmod 600 ~/.onedrive-mcp/credentials.json
```

## Notes

- **Item IDs**: stable per drive. The `id` field is the full Graph ID — pass it as-is.
- **Path addressing**: use `/` separators (`Documents/Reports/q4.xlsx`). Scripts handle URL-encoding.
- **Conflict behavior**: uploads default to `replace`. Use the API directly for `rename` / `fail`.
- **Large uploads**: files > 4 MiB automatically use a resumable upload session (10 MiB chunks).
- **Download URLs**: `@microsoft.graph.downloadUrl` returned by the API is pre-authenticated and short-lived (minutes).
- **Deletes** move to the recycle bin (recoverable via the web UI for 30 days personal / 93 days business).
- **Throttling**: respect the `Retry-After` header on `429`.

## Troubleshooting

**"Token expired"** → `./scripts/onedrive-token.sh refresh`

**"Invalid grant"** → Refresh token revoked or expired; re-run `onedrive-setup.sh` (or have the deployment system re-bootstrap).

**"accessDenied"** → Token's scopes don't cover the operation. Check `onedrive-token.sh info` and reconsent with the right scopes.

**"itemNotFound" on a visible path** → URL-encode special chars. Try `info <id>` to confirm the ID-based path works.

**SharePoint drive returns 404 for `/me/drive`** → Use `/sites/{site-id}/drive` or list `/me/drives` first.

**Resumable upload stalls** → The `uploadUrl` expired (~1h). Restart the session via `upload` (the script re-creates it automatically).

## Supported Accounts

- Personal Microsoft accounts (`outlook.com`, `hotmail.com`, `live.com`)
- Work / school accounts (Microsoft 365) — may require admin consent for `*.All` scopes
- SharePoint document libraries via `Sites.ReadWrite.All`

## Resources

- [Microsoft Graph OneDrive overview](https://learn.microsoft.com/en-us/graph/api/resources/onedrive)
- [DriveItem resource](https://learn.microsoft.com/en-us/graph/api/resources/driveitem)
- [Large file upload (resumable)](https://learn.microsoft.com/en-us/graph/api/driveitem-createuploadsession)
- [Sharing concepts](https://learn.microsoft.com/en-us/graph/api/resources/sharing)
- `references/api-reference.md` — full endpoint catalog
- `references/permissions.md` — OAuth scopes (delegated + application)
- `references/setup.md` — manual Azure Portal walkthrough

## Changelog

### v1.0.0
- Initial release
- Direct Microsoft Graph integration (no third-party proxy)
- Three install paths: automated (Azure CLI), manual (portal), or headless bootstrap (pre-provisioned tokens)
- File/folder CRUD, sharing, permissions, search, recent, shared-with-me, versions, thumbnails, preview, delta
- BYO-token support via `ONEDRIVE_ACCESS_TOKEN` or `onedrive-token.sh set`
- Multi-drive targeting via `ONEDRIVE_DRIVE_PREFIX`
