# Setup Guide: 1Password for OpenClaw

Step-by-step instructions for setting up 1Password integration with OpenClaw. Written for both humans and AI agents.

---

## Prerequisites

- A **1Password Business or Teams** plan (required for service accounts)
- Admin access to your 1Password account
- Node.js 18+
- OpenClaw installed

## Overview

```
You need three things:
1. A custom vault in 1Password (to store your secrets)
2. A service account (headless access for agents)
3. The plugin installed and configured in OpenClaw
```

---

## Step 1: Create a Custom Vault

Service accounts **cannot** access built-in vaults (Shared, Employee, Private). You must create a custom vault.

### Via 1Password.com (web)

1. Sign in to your 1Password account
2. Click **New Vault** in the sidebar (or **+** button)
3. Name it `Agent Secrets` (or whatever you prefer)
4. Click **Create Vault**

### Via CLI

```bash
op vault create "Agent Secrets" --description "API keys for OpenClaw agents"
```

---

## Step 2: Add Secrets to the Vault

Add the API keys your agents need.

### Via 1Password.com (web)

1. Open the **Agent Secrets** vault
2. Click **New Item** → **API Credential**
3. Title: `OpenAI API`
4. Add a field named `api key` with your OpenAI key as the value
5. Repeat for other secrets (e.g. `Anthropic Auth Token`)

### Via CLI

```bash
op item create --category "API Credential" --title "OpenAI API" \
  --vault "Agent Secrets" 'api key=sk-proj-YOUR_KEY_HERE'

op item create --category "API Credential" --title "Anthropic Auth Token" \
  --vault "Agent Secrets" 'api key=sk-ant-YOUR_TOKEN_HERE'
```

---

## Step 3: Enable Service Accounts (Admin — One Time)

If this is your first service account, an admin must enable the feature.

### Via 1Password.com (web)

1. Sign in as an **owner or admin**
2. Go to **Policies** (in sidebar) → **Developer**
3. Under **Service Accounts**, ensure they're enabled
4. Under **Permissions**, configure which groups can create service accounts

If you see a 403 error when creating a service account, this step was missed.

---

## Step 4: Create a Service Account

**Important:** Service account permissions are **immutable after creation**. You cannot add vault access or change permissions later. If you need different permissions, you must create a new service account.

### Via 1Password.com (web)

1. Sign in to 1Password.com
2. Navigate to **Developer** → **Directory** (in sidebar)
3. Under "Infrastructure Secrets Management", select **Other**
4. Click **Create a Service Account**
5. **Name**: `OpenClaw Agent`
6. **Create vaults**: No (unless you want agents to create vaults)
7. **Vault access**: Select `Agent Secrets`
8. **Click the settings/gear icon** next to `Agent Secrets` to choose permissions:
   - `read_items` — required (lets agents read secrets)
   - `write_items` — optional (lets agents create/update secrets)
9. Click **Create Account**
10. **CRITICAL: Copy the token immediately.** It starts with `ops_` and is shown only once.
11. Click **Save in 1Password** to store a backup of the token

### Via CLI

For read-only access:
```bash
op service-account create "OpenClaw Agent" \
  --expires-in 0 \
  --vault "Agent Secrets:read_items"
```

For read + write access:
```bash
op service-account create "OpenClaw Agent" \
  --expires-in 0 \
  --vault "Agent Secrets:read_items,write_items"
```

For multiple vaults:
```bash
op service-account create "OpenClaw Agent" \
  --expires-in 0 \
  --vault "Agent Secrets:read_items,write_items" \
  --vault "Production Keys:read_items"
```

The command outputs a token starting with `ops_...`. Save it immediately.

### Changing Permissions

You **cannot** modify an existing service account's permissions. To change them:

1. Create a **new** service account with the desired permissions
2. Save the new token to `~/.openclaw/secrets/op-sa-token`
3. Delete the old service account from **Developer** → **Directory** in 1Password.com

---

## Step 5: Save the Service Account Token

```bash
mkdir -p ~/.openclaw/secrets
```

Write the `ops_...` token into the file (use a text editor, or):
```bash
# Replace ops_YOUR_TOKEN with the actual token
echo "ops_YOUR_TOKEN" > ~/.openclaw/secrets/op-sa-token
chmod 600 ~/.openclaw/secrets/op-sa-token
```

**Verify the file:**
```bash
# Should show the token starts with ops_
head -c 4 ~/.openclaw/secrets/op-sa-token
# Expected output: ops_
```

---

## Step 6: Install the Plugin

### From npm (when published)

```bash
openclaw plugins install @wipcomputer/wip-1password
```

### From local build

```bash
cd /path/to/openclaw-1password
npm install && npm run build
cp -r . ~/.openclaw/extensions/1password/
```

---

## Step 7: Enable in OpenClaw Config

Add to `~/.openclaw/openclaw.json` (merge with existing config):

```json
{
  "plugins": {
    "entries": {
      "1password": {
        "enabled": true,
        "config": {
          "defaultVault": "Agent Secrets"
        }
      }
    }
  }
}
```

---

## Step 8: Test

```bash
# Test 1Password connectivity
openclaw op-secrets test
# Expected: "1Password connection OK — 1 vault(s): Agent Secrets (...)"

# Read a secret (shows redacted preview)
openclaw op-secrets read "OpenAI API"
# Expected: "Agent Secrets/OpenAI API/api key: sk-pro...[154 chars]...EEwA"
```

---

## Step 9: Replace Plaintext Keys with `op://` References

In `openclaw.json`, replace plaintext API keys:

**Before:**
```json
"apiKey": "sk-proj-hTYw...actual-key...EEwA"
```

**After:**
```json
"apiKey": "op://Agent Secrets/OpenAI API/api key"
```

The plugin resolves these at startup. The real key stays in 1Password, never on disk.

### What CAN use `op://` refs

- Any value in `openclaw.json` — resolved at startup by the plugin's resolver service

### What CANNOT use `op://` refs

- `auth-profiles.json` — loaded by a separate OpenClaw subsystem that plugins can't hook into
- Any file outside of `openclaw.json`

---

## Troubleshooting

### "Token file not found"
The file `~/.openclaw/secrets/op-sa-token` doesn't exist or is empty.
```bash
ls -la ~/.openclaw/secrets/op-sa-token
```

### "Token doesn't look like a service account token"
The file exists but doesn't start with `ops_`. It might contain whitespace, a newline, or the wrong token.
```bash
head -c 10 ~/.openclaw/secrets/op-sa-token
```

### "Vault not found"
Service accounts can only access **custom** vaults. Built-in vaults (Shared, Employee, Private) are not supported.
```bash
openclaw op-secrets test  # lists accessible vaults
```

### "403 Forbidden" creating a service account
An admin needs to enable service accounts. See [Step 3](#step-3-enable-service-accounts-admin--one-time).

### "not sufficient permissions for the item update operation"
The service account has `read_items` but not `write_items`. Service account permissions are immutable — you must create a new service account with write access. See [Step 4: Changing Permissions](#changing-permissions).

### "Granting a service account access to the Team/Shared vault is not supported"
You're trying to use a built-in vault. Create a custom vault instead. See [Step 1](#step-1-create-a-custom-vault).

### Plugin not loading
Check that:
1. The plugin is in `~/.openclaw/extensions/` or installed via `openclaw plugins install`
2. `openclaw.json` has `"1password": { "enabled": true }` under `plugins.entries`
3. Run `openclaw doctor` to check for plugin errors

---

## Quick Reference

| Item | Value |
|------|-------|
| Token location | `~/.openclaw/secrets/op-sa-token` |
| Token prefix | `ops_` |
| Config key | `plugins.entries.1password` |
| Default vault | `Agent Secrets` (configurable) |
| Secret ref format | `op://Vault Name/Item Title/field name` |
| Service account permissions | Immutable after creation |

### Agent Tools

| Tool | Purpose | Permissions Needed |
|------|---------|-------------------|
| `op_read_secret` | Read a secret | `read_items` |
| `op_list_items` | List vault items | `read_items` |
| `op_write_secret` | Create/update secret | `read_items` + `write_items` |

### CLI Commands

| Command | Purpose |
|---------|---------|
| `openclaw op-secrets test` | Verify connectivity |
| `openclaw op-secrets read <item>` | Read secret (redacted) |
| `openclaw op-secrets resolve <file>` | Dry-run op:// resolution |
