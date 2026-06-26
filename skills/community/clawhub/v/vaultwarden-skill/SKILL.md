# Vaultwarden Skill

Manage secrets in Vaultwarden via wrapper scripts. All scripts handle session state, caching, logging, and error handling — do not call `bw` directly.

## CLI Version Requirement — CRITICAL

Bitwarden CLI 2024.x+ breaks Vaultwarden authentication with `User Decryption Options are required`.

```bash
# Install the required version
npm install -g @bitwarden/cli@2023.10.0

# Verify
bw --version  # must show 2023.10.0
```

`vw-unlock.sh` will hard-exit if an incompatible version is detected.

## Setup (run once)

```bash
bw config server https://vaultwarden.mbojer.dk
```

## Required Environment Variables

Set in OpenClaw config, never stored in vault:

| Variable | Purpose |
|---|---|
| `BW_CLIENTID` | API key client ID |
| `BW_CLIENTSECRET` | API key client secret |
| `BW_PASSWORD` | Master password for unlock |
| `VW_COLLECTION_NAME` | Collection name to scope to (default: `openclaw`) — org accounts only |
| `VW_COLLECTION_ID` | Hardcode collection ID — use if name lookup fails (org accounts only) |
| `VW_SESSION_DIR` | Session token dir (default: `/run/openclaw/vw`) |
| `VW_LOG_FILE` | Audit log path (default: `/var/log/openclaw/vaultwarden.log`) |
| `VW_CACHE_TTL` | Read cache TTL in seconds (default: `60`, set `0` to disable) |

## Collection Scoping — Personal vs Org Vaults

Personal Vaultwarden accounts cannot access collections via API key — this is a Bitwarden limitation, not a bug in this skill. `bw list collections` returns `[]` on personal vaults.

The skill handles this automatically: if no collection is found, all operations fall back to unscoped (full vault) queries. For org accounts, set `VW_COLLECTION_NAME` or `VW_COLLECTION_ID` to scope operations to a specific collection.


## Session Management

```bash
vw-unlock.sh    # authenticate and unlock — run before any vault operation
vw-lock.sh      # lock vault and clear all caches
vw-status.sh    # check connection and session state
vw-sync.sh      # sync local cache with server — run if vault modified externally
```

Session token stored in `$VW_SESSION_DIR/.bw_session` (chmod 600).
Collection ID cached in `$VW_SESSION_DIR/.collection_id` — invalidated on lock and sync.
Read cache stored in `$VW_SESSION_DIR/cache/` — TTL controlled by `VW_CACHE_TTL`.

## Read Operations

All reads are collection-scoped to `$VW_COLLECTION_NAME`. Frequently-read items are cached with a TTL to reduce API calls.

```bash
vw-list.sh [query]               # list items in openclaw collection, optional search
vw-get.sh <name|id>              # full item JSON
vw-get-pass.sh <n>               # password only (collection-scoped, cached)
vw-get-user.sh <n>               # username only (collection-scoped, cached)
vw-get-field.sh <n> <field>      # single custom field value
vw-get-totp.sh <n>               # current TOTP code (not cached — codes expire)
```

## Write Operations

Write operations invalidate the read cache automatically.

```bash
echo <pass> | vw-create-login.sh <n> <user>     # create login item (password via stdin)
echo <content> | vw-create-note.sh <n>           # create secure note (content via stdin)
echo <value> | vw-update.sh <id> <field>         # update field: password|username|notes|custom:<n>
vw-delete.sh <id> <expected name>                # move to trash — requires both ID and name to match
vw-rotate-pass.sh <name|id> [length]             # generate new password and update atomically
```

Capture rotated password cleanly (status goes to stderr):
```bash
NEW_PASS=$(vw-rotate-pass.sh "MyService")
```

## Rules

- Always run `vw-unlock.sh` before vault operations, `vw-lock.sh` when done
- Run `vw-sync.sh` before reads if vault was modified via web UI or another client
- Always use item ID (not name) for `vw-update.sh` and `vw-delete.sh`
- `vw-delete.sh` moves items to trash — not permanent. Empty trash via web UI if needed
- All secret values must be passed via stdin — never as CLI arguments
- Never log or output raw secret values — only names, IDs, and operation results
- If any script exits non-zero, stop and report — do not retry silently
- All operations are scoped to `$VW_COLLECTION_NAME` when a collection is available. Personal vaults (no org) fallback to full vault — no collection required

## Error Reference

| Error | Fix |
|---|---|
| `bw CLI X.X.X is incompatible` | `npm install -g @bitwarden/cli@2023.10.0` |
| `User Decryption Options are required` | Same as above — wrong CLI version |
| `no active session` | Run `vw-unlock.sh` |
| `session invalid or expired` | Run `vw-unlock.sh` |
| `collection not found` | Check `VW_COLLECTION_NAME`, run `vw-sync.sh` |
| `name mismatch` | Verify item ID with `vw-get.sh` before deleting |
| `custom field does not exist` | Check field name with `vw-get.sh` |
| `server not configured` | Run `bw config server https://vaultwarden.mbojer.dk` |
| `API key login failed` | Check `BW_CLIENTID` and `BW_CLIENTSECRET` |
