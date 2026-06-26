---
name: wip-1password
description: AI plugin (Claude Code, OpenClaw) for 1Password secrets via JS SDK. Resolves op:// references at startup, provides agent tools for reading/writing secrets, fully headless via service account.
license: MIT
interface: [module, mcp, openclaw-plugin, skill]
metadata:
  display-name: "1Password Secrets"
  version: "0.2.2".2.1"
  homepage: "https://github.com/wipcomputer/wip-1password"
  author: "Parker Todd Brooks"
  category: security
  capabilities:
    - resolve-op-refs
    - read-secrets
    - write-secrets
    - list-vault-items
  requires:
    bins: [node, npm]
    services: [1password-service-account]
  openclaw:
    requires:
      bins: [node, npm]
      plugins: [op-secrets]
    install:
      - id: node
        kind: node
        package: "@wipcomputer/wip-1password"
        label: "Install via npm"
    emoji: "🔐"
compatibility: Requires Node.js 18+, 1Password with service account support (all plans). OpenClaw 2026.1+.
---

# wip-1password

AI plugin (Claude Code, OpenClaw) for 1Password secrets. Uses the official JavaScript SDK with service accounts for fully headless operation... no desktop app, no biometrics, no popups.

## When to Use This Skill

**Use wip-1password for:**
- Resolving `op://` secret references in config files at startup
- Reading API keys, tokens, and credentials from 1Password at runtime
- Storing new secrets in 1Password vaults
- Listing available secrets in a vault

### Do NOT Use For

- Managing 1Password accounts or users (use the 1Password admin console)
- Accessing built-in vaults (Shared, Employee, Private). Service accounts only work with custom vaults.
- Repos that don't use OpenClaw (use the `op` CLI directly instead)

## API Reference

### OpenClaw Plugin (startup resolver)

Resolves `op://vault/item/field` strings in `openclaw.json` at boot. Values exist in memory only... never written to disk.

```jsonc
// In openclaw.json
"someService": {
  "apiKey": "op://Agent Secrets/Some Service/api key"
}
```

### Agent Tools

```
op_read_secret({ item: "OpenAI API", vault: "Agent Secrets", field: "api key" })
op_list_items({ vault: "Agent Secrets" })
op_write_secret({ item: "New Key", value: "sk-...", vault: "Agent Secrets" })
```

### Module

```typescript
import { resolveSecretRefs } from "@wipcomputer/wip-1password";

const resolved = await resolveSecretRefs({
  apiKey: "op://Agent Secrets/OpenAI API/api key",
});
```

## Setup

```bash
# 1. Save service account token
mkdir -p ~/.openclaw/secrets
echo "ops_..." > ~/.openclaw/secrets/op-sa-token
chmod 600 ~/.openclaw/secrets/op-sa-token

# 2. Enable in openclaw.json
# plugins.entries.op-secrets.enabled = true
# plugins.entries.op-secrets.config.defaultVault = "Agent Secrets"

# 3. Test
openclaw op-secrets test
```

## Key Rules

- **Never call `op` bare.** Always prefix with `OP_SERVICE_ACCOUNT_TOKEN`.
- **Never log secret values.** Store in variables only.
- **Leave `memorySearch.remote` as `{}`** ... the plugin sets `process.env.OPENAI_API_KEY` instead.
- **Service account token:** Always at `~/.openclaw/secrets/op-sa-token`.
- **Custom vaults only.** Service accounts can't access built-in vaults.
