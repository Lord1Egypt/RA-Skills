<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Attio API: Workspace blocklist

## `attio api workspace-blocklist-addresses-delete [options]`

- What: Delete a workspace blocklist address
- Call: `DELETE /v2/workspace_blocklist_addresses/{address}`, effect: destructive
- Sign-in: oauth2 (email\_calendar\_blocklist:read-write)
- Permission keys: `attio.delete`

| Flag | Required | What |
|---|---|---|
| `--address <value>` | yes | address |

## `attio api workspace-blocklist-addresses-list [options]`

- What: List workspace blocklist addresses
- Call: `GET /v2/workspace_blocklist_addresses`, effect: read
- Sign-in: oauth2 (email\_calendar\_blocklist:read)
- Pages: cursor: send `cursor` (query), read the next one from `pagination.next_cursor`; items in `data`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--limit <value>` | no | limit |
| `--cursor <value>` | no | cursor |
| `--all` | no | read every page, as the API pages it |

## `attio api workspace-blocklist-addresses-replace [options]`

- What: Add or update workspace blocklist addresses
- Call: `PUT /v2/workspace_blocklist_addresses`, effect: write
- Sign-in: oauth2 (email\_calendar\_blocklist:read-write)
- Body: `PutV2WorkspaceBlocklistAddressesRequest`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
