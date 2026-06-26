# Status: openclaw-1password

This document tracks what's been done and what remains.

---

## Completed

### Plugin core (all working)
- `op_read_secret` tool — tested, working
- `op_list_items` tool — tested, working
- `op_write_secret` tool — implemented, **not yet tested** (service account may need `write_items`)
- CLI: `test`, `read`, `resolve` commands — all working
- `resolveSecretRefs` utility — working, exported
- Lazy SDK client with token validation — working
- SKILL.md — written

### Config secret resolution
- Startup service (`op-secret-resolver`) resolves `op://` refs in `openclaw.json`
- `openclaw.json` uses `op://Agent Secrets/OpenAI API/api key` for the OpenAI key
- Resolved in memory at boot — plaintext never on disk

### Infrastructure
- 1Password Business plan on `wipcomputer.1password.com`
- Custom "Agent Secrets" vault (ID: `ywmget6o6aki6wh2e4slzvrr5a`)
- Service account "OpenClaw Agent" with `read_items` access
- Token at `~/.openclaw/secrets/op-sa-token` (chmod 600)

---

## Remaining

### 1. Test `op_write_secret` against real vault

The write tool is implemented but never tested live.

**Steps:**
1. Verify connectivity: `openclaw op-secrets test`
2. Test creating a new item via agent tool `op_write_secret`:
   - `item`: "Test Secret", `value`: "test-value-12345"
3. Verify: `openclaw op-secrets read "Test Secret"`
4. Test updating: call `op_write_secret` again with `value`: "updated-value-67890"
5. Clean up: delete "Test Secret" from 1Password UI

**If it fails:** The service account likely needs `write_items`. Recreate it:
```bash
op service-account create "OpenClaw Agent" \
  --expires-in 0 \
  --vault "Agent Secrets:read_items,write_items" \
  --account wipcomputer.1password.com
```
Then update the token at `~/.openclaw/secrets/op-sa-token`.

### 2. Publish to npm (optional)

The package is structured for npm publishing but not yet published.

```bash
cd /Users/lesa/Documents/Projects/Claude\ Code/openclaw-1password
npm run build
npm publish --access public
```

Requires an npm account with a scope (e.g. `@openclaw`).

---

## Known Limitation: auth-profiles.json

`auth-profiles.json` is loaded by a separate OpenClaw subsystem that plugins cannot hook into. The resolver service only has access to `ctx.config` (which corresponds to `openclaw.json`).

**Consequence:** The Anthropic token in `auth-profiles.json` must remain as plaintext. It cannot use `op://` references.

**To fix this properly:** OpenClaw core would need to support a "secret provider" hook in its auth profile loader. This is a feature request for OpenClaw, not something the plugin can solve.

**Current state of secrets on disk:**

| File | Secret | Storage | Status |
|------|--------|---------|--------|
| `openclaw.json` | OpenAI API key | `op://` reference | No plaintext on disk |
| `auth-profiles.json` | Anthropic token | Plaintext | Cannot use `op://` |
| `auth-profiles.json` | OpenAI OAuth tokens | Plaintext (auto-managed) | OAuth, not static secrets |

---

## Reference

### Service account
- **Account**: wipcomputer.1password.com
- **Service account**: "OpenClaw Agent"
- **Token**: `~/.openclaw/secrets/op-sa-token` (chmod 600)
- **Vault**: "Agent Secrets" (custom vault)
- **Permissions**: `read_items` (may need `write_items` for write tool)

### Secrets in vault
| Item | Field | What it is |
|------|-------|------------|
| OpenAI API | api key | OpenAI project API key |
| Anthropic Auth Token | api key | Anthropic auth token |

### File locations
- **Repo**: `/Users/lesa/Documents/Projects/Claude Code/openclaw-1password/`
- **Live extension**: `~/.openclaw/extensions/op-secrets/` (loads `index.ts` directly)
- **Source**: `src/index.ts`

### Live extension vs repo

The live extension at `~/.openclaw/extensions/op-secrets/` uses plugin ID `"op-secrets"` and config key `plugins.entries["op-secrets"]`. The repo uses plugin ID `"1password"` and config key `plugins.entries["1password"]`. These are independent — the live extension is a local install, the repo is for distribution.
