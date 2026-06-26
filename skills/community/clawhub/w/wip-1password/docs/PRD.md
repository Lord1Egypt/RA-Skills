# PRD: openclaw-1password

## Problem

OpenClaw agents need API keys and secrets (Anthropic, OpenAI, etc.) to function. Today, these credentials are stored as **plaintext** in configuration files:

- `openclaw.json` (e.g., `memorySearch.remote.apiKey`)
- `agents/main/agent/auth-profiles.json` (provider tokens)
- `.env` files or environment variables

This creates several risks:

1. **Leakage into logs**: Agent session logs (`.jsonl`) capture tool calls and responses. Secrets passed through config end up serialized into these logs in plaintext.
2. **No rotation**: Changing a key means editing config files manually across every machine.
3. **No audit trail**: No record of which agent accessed which secret, when.
4. **No access control**: Any process running as the user can read the config files.

## Solution

An OpenClaw plugin (`@wipcomputer/wip-1password`) that integrates with **1Password** via the official JavaScript SDK. Agents retrieve secrets at runtime from a 1Password vault using a service account — fully headless, no desktop app or biometric prompts required.

## Target Users

- OpenClaw users who manage API keys for multiple providers
- Teams running OpenClaw agents on servers, CI/CD, or unattended machines
- Anyone who wants to stop storing plaintext secrets in config files

## Requirements

### Implemented (P0)

1. **Agent tool: `op_read_secret`** — Reads a single secret value from 1Password given vault, item, and field names. Returns the secret to the agent in memory (never written to disk).

2. **Agent tool: `op_list_items`** — Lists items in a vault so agents can discover available secrets.

3. **Agent tool: `op_write_secret`** — Creates or updates a secret in 1Password. Supports both creating new items and updating existing fields. Requires `write_items` permission on the service account.

4. **Service account auth** — Uses a 1Password service account token for headless operation. Token stored in a local file with `600` permissions.

5. **CLI commands** — `openclaw op-secrets test` (verify connectivity), `openclaw op-secrets read <item>` (read with redacted preview), `openclaw op-secrets resolve <file>` (dry-run showing which `op://` refs would resolve).

6. **Skill file** — `SKILL.md` that teaches agents what tools are available and the guardrails (never log secret values).

7. **Config secret resolution** — A startup service that resolves `op://vault/item/field` references in `openclaw.json` to real values in memory. Enables replacing plaintext API keys in config with `op://` URIs.

8. **`resolveSecretRefs` utility** — Exported function that walks any JS object tree and resolves `op://` strings. Usable by other plugins or scripts.

9. **Configurable token path** — Token file location configurable via plugin config or `OP_SA_TOKEN_PATH` environment variable.

10. **Configurable default vault** — Default vault name set in plugin config, overridable per tool call.

11. **Lazy SDK client** — The 1Password SDK client is initialized on first use, not at plugin load time. Avoids blocking startup if the token is missing.

12. **Graceful degradation** — If the token file is missing or invalid, tools return clear error messages instead of crashing the gateway.

### Not Possible Without Core Changes

13. **Auth profile secret resolution** — `auth-profiles.json` is loaded by a separate OpenClaw subsystem that plugins cannot hook into. Secrets in that file (Anthropic token, OpenAI OAuth tokens) must remain as plaintext. Fixing this requires OpenClaw core to support a "secret provider" hook in its auth profile loader.

### Nice to Have (P2)

14. **npm-publishable** — Installable via `openclaw plugins install @wipcomputer/wip-1password`. Package structure is ready but not yet published.

15. **Multiple vault support** — Service account with access to multiple vaults (already supported by the code, just needs the SA configured with access to multiple vaults).

## Architecture

```
1Password Cloud
    ^
    |  HTTPS (SDK)
    |
@1password/sdk client  (singleton, lazy-init)
    ^
    |  reads token from file
    |
~/.openclaw/secrets/op-sa-token  (chmod 600)
    |
openclaw-1password plugin
    |
    +-- op_read_secret tool     (agent-facing)
    +-- op_list_items tool      (agent-facing)
    +-- op_write_secret tool    (agent-facing, needs write_items)
    +-- op-secret-resolver      (startup service, resolves op:// in config)
    +-- openclaw op-secrets     (CLI for human debugging)
    +-- resolveSecretRefs()     (exported utility)
    +-- SKILL.md                (agent knowledge)
```

### Scope of Secret Resolution

```
openclaw.json (ctx.config)
  └── Any op:// string → ✅ Resolved at startup by plugin service

auth-profiles.json
  └── Provider tokens → ❌ Cannot resolve (separate subsystem)
                          Requires OpenClaw core "secret provider" hook
```

### 1Password Setup (User Responsibility)

1. 1Password **Business** or **Teams** plan (required for service accounts)
2. A **custom vault** (e.g., "Agent Secrets") — service accounts cannot access built-in Shared/Employee vaults
3. A **service account** with `read_items` access (add `write_items` for write support)
4. Service account token saved to `~/.openclaw/secrets/op-sa-token`

### Plugin Lifecycle

1. **Load**: OpenClaw discovers plugin via `openclaw.plugin.json` manifest
2. **Register**: Plugin registers tools, CLI commands, and startup service
3. **Startup service**: Walks `ctx.config`, resolves `op://` refs in memory
4. **First tool use**: On first `op_read_secret` call, reads token from disk, creates SDK client (if not already created by the resolver)
5. **Resolve**: Calls `client.secrets.resolve("op://<vault>/<item>/<field>")`
6. **Return**: Secret value returned to agent in tool response (in memory only)

## Non-Goals

- **Desktop app integration**: We explicitly avoid the `op` CLI and desktop app. The whole point is headless operation.
- **Token generation**: The plugin does not create service accounts. That's a one-time admin setup.
- **Secret rotation**: Out of scope. Users rotate secrets in 1Password; the plugin always reads the current value.
- **Caching**: Secrets are fetched fresh on every call. 1Password SDK handles connection pooling internally.
- **Auth profile resolution**: Out of scope for the plugin. Requires OpenClaw core changes.

## Success Criteria

1. `openclaw op-secrets test` shows vault connectivity
2. Agent calls `op_read_secret` and receives the correct value
3. `openclaw.json` can use `op://` references instead of plaintext keys
4. No secret values appear in session logs, config files on disk, or CLI output
5. Plugin works after reboot with no human intervention
6. Plugin loads in <500ms, secret resolution in <2s

## Dependencies

- `@1password/sdk` (^0.3.x) — 1Password JavaScript SDK
- Node.js 18+ (SDK requirement)
- OpenClaw plugin SDK (`openclaw/plugin-sdk`)
