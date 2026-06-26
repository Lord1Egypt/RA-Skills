# Development Guide: openclaw-1password

Step-by-step instructions for building this plugin from scratch. Each step is self-contained — an agent or developer can follow them sequentially.

---

## Prerequisites

Before starting, confirm:

- Node.js 18+ installed
- OpenClaw installed (`openclaw --version`)
- A 1Password Business or Teams account
- A 1Password service account token (see [1Password Setup](#step-0-1password-setup))

---

## Step 0: 1Password Setup

This is a one-time admin task, not code.

### 0.1 Create a custom vault

Service accounts **cannot** access built-in vaults (Shared, Employee, Private). You must create a custom vault.

```bash
op vault create "Agent Secrets" --description "API keys for OpenClaw agents"
```

### 0.2 Add secrets to the vault

```bash
op item create --category "API Credential" --title "OpenAI API" \
  --vault "Agent Secrets" 'api key=sk-...'

op item create --category "API Credential" --title "Anthropic Auth Token" \
  --vault "Agent Secrets" 'api key=sk-ant-...'
```

### 0.3 Create a service account

```bash
op service-account create "OpenClaw Agent" \
  --expires-in 0 \
  --vault "Agent Secrets:read_items"
```

This outputs a token starting with `ops_...`. Save it:

```bash
mkdir -p ~/.openclaw/secrets
# Paste the token into this file:
nano ~/.openclaw/secrets/op-sa-token
chmod 600 ~/.openclaw/secrets/op-sa-token
```

### 0.4 Verify

```bash
export OP_SERVICE_ACCOUNT_TOKEN=$(cat ~/.openclaw/secrets/op-sa-token)
op vault list     # should show "Agent Secrets"
op item list --vault "Agent Secrets"  # should show your items
unset OP_SERVICE_ACCOUNT_TOKEN
```

---

## Step 1: Project Scaffolding

### 1.1 Initialize the project

```bash
mkdir openclaw-1password && cd openclaw-1password
git init
npm init -y
```

### 1.2 Create `package.json`

Overwrite the generated `package.json` with:

```json
{
  "name": "@wipcomputer/wip-1password",
  "version": "0.1.0",
  "description": "OpenClaw plugin for 1Password secrets via JS SDK",
  "type": "module",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "files": ["dist", "skills", "openclaw.plugin.json"],
  "openclaw": {
    "extensions": ["./dist/index.js"]
  },
  "scripts": {
    "build": "tsup src/index.ts --format esm --dts",
    "dev": "tsup src/index.ts --format esm --dts --watch",
    "prepublishOnly": "npm run build"
  },
  "keywords": ["openclaw", "openclaw-plugin", "1password", "secrets"],
  "license": "MIT",
  "peerDependencies": {
    "openclaw": ">=2026.1.0"
  },
  "dependencies": {
    "@1password/sdk": "^0.3.1"
  },
  "devDependencies": {
    "tsup": "^8.0.0",
    "typescript": "^5.4.0",
    "openclaw": "*"
  }
}
```

Key points:
- `"openclaw.extensions"` tells OpenClaw where to find the plugin entry point
- `"files"` controls what gets published to npm
- `tsup` bundles TypeScript to ESM for distribution
- `openclaw` is a peer dependency (the host provides it)

### 1.3 Create `tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "declaration": true,
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src"]
}
```

### 1.4 Create `openclaw.plugin.json`

```json
{
  "id": "1password",
  "name": "1Password Secrets",
  "description": "Read secrets from 1Password via JS SDK (headless, service account)",
  "skills": ["./skills"],
  "configSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "defaultVault": { "type": "string" },
      "tokenPath": { "type": "string" }
    }
  },
  "uiHints": {
    "defaultVault": {
      "label": "Default Vault",
      "placeholder": "Agent Secrets"
    },
    "tokenPath": {
      "label": "Service Account Token Path",
      "placeholder": "~/.openclaw/secrets/op-sa-token",
      "sensitive": true
    }
  }
}
```

### 1.5 Create `.gitignore`

```
node_modules/
dist/
*.tgz
```

### 1.6 Install dependencies

```bash
npm install
```

---

## Step 2: Plugin Entry Point (`src/index.ts`)

This is the core of the plugin. It has three parts:

### 2.1 SDK Client (lazy singleton)

```typescript
import { readFileSync } from "node:fs";
import { createClient, type Client } from "@1password/sdk";
```

Create a `getClient()` function that:
- Reads the service account token from the configured file path
- Calls `createClient({ auth: token, integrationName: "OpenClaw", integrationVersion: "<pkg version>" })`
- Caches the client in a module-level variable (lazy singleton)
- Throws a clear error if the token file doesn't exist

### 2.2 Helper functions

Create three helpers:

1. **`resolveSecret(vault, item, field)`** — Calls `client.secrets.resolve(\`op://${vault}/${item}/${field}\`)`. This is the SDK's secret reference format.

2. **`listVaults()`** — Calls `client.vaults.list()`. Returns an array of vault objects with `id` and `title`.

3. **`listItems(vaultId)`** — Calls `client.items.list(vaultId)`. Returns an array of item objects with `id`, `title`, and `category`.

### 2.3 Plugin registration

Export a default plugin object with:
- `id`, `name`, `description`, `configSchema` (matching the manifest)
- `register(api)` function that:

**Reads config:**
```typescript
const pluginConfig = (api.config as any)?.plugins?.entries?.["1password"]?.config;
const defaultVault = pluginConfig?.defaultVault || "Agent Secrets";
const tokenPath = pluginConfig?.tokenPath || `${process.env.HOME}/.openclaw/secrets/op-sa-token`;
```

**Registers `op_read_secret` tool:**
- Parameters: `item` (required string), `vault` (optional string), `field` (optional string, default `"api key"`)
- Execute: calls `resolveSecret()`, returns value as text content
- Registered as `{ optional: true }` — requires allowlisting
- Error handling: catch and return `{ isError: true }` with message

**Registers `op_list_items` tool:**
- Parameters: `vault` (optional string)
- Execute: finds vault by name, calls `listItems(vault.id)`, formats as `title (category)` lines
- Registered as `{ optional: true }`

**Registers CLI commands:**
- `openclaw op-secrets test` — calls `listVaults()`, prints vault names
- `openclaw op-secrets read <item>` — calls `resolveSecret()`, prints redacted preview (first 6 chars + length + last 4 chars)

### 2.4 `resolveSecretRefs` utility

Create and export a `resolveSecretRefs<T>(obj: T): Promise<T>` function that:
- Recursively walks any JS object
- For any string matching `op://vault/item/field`, resolves it via `resolveSecret()`
- Returns a new object with resolved values (non-matching values pass through)
- Handles arrays and nested objects

This is the core utility that the startup service uses, and is also exported for programmatic use by other plugins.

### 2.5 Write tool (`op_write_secret`)

Registers an `op_write_secret` tool that:
- Parameters: `item` (required), `value` (required), `vault` (optional), `field` (optional, default `"api key"`)
- Checks if item already exists in the vault (case-insensitive title match)
- If exists: gets the full item, finds/updates the field, puts it back via `client.items.put()`
- If new: creates via `client.items.create()` with `ItemCategory.ApiCredentials` and `ItemFieldType.Concealed`
- Registered as `{ optional: true }`
- Requires `write_items` permission on the service account

### 2.6 Startup service (`op-secret-resolver`)

Register a service via `api.registerService()` that runs at OpenClaw startup:
```typescript
api.registerService?.({
  id: "op-secret-resolver",
  async start(ctx: any) {
    const resolved = await resolveSecretRefs(ctx.config);
    Object.assign(ctx.config, resolved);
  },
});
```

This resolves `op://` references in `openclaw.json` (the main config). Note:
- Uses `Object.assign` for shallow merge — works because `resolveSecretRefs` returns a full deep copy
- Only resolves `ctx.config` — cannot resolve `auth-profiles.json` (separate subsystem)
- Runs before agents start, so resolved values are available immediately

### 2.7 CLI resolve command

Add a third CLI command `openclaw op-secrets resolve <file>` that:
- Reads a JSON file, resolves `op://` refs (dry run)
- Shows which keys were resolved with redacted values
- Useful for verifying which refs exist in a config file

---

## Step 3: Skill File (`skills/op-secrets/SKILL.md`)

Create `skills/op-secrets/SKILL.md` with YAML frontmatter:

```yaml
---
name: op-secrets
description: Read secrets from 1Password using the op-secrets plugin tools.
metadata:
  openclaw:
    emoji: "\U0001F510"
    requires:
      plugins: ["1password"]
---
```

The body should document:
- Both tools and their parameters
- Example items that might be in the vault
- **Guardrails**: Never log, echo, or paste secret values into chat/logs/code. Store in variables only.

---

## Step 4: Build and Test Locally

### 4.1 Build

```bash
npm run build
```

Verify `dist/index.js` and `dist/index.d.ts` exist.

### 4.2 Link for local testing

```bash
# Copy to extensions directory
cp -r . ~/.openclaw/extensions/1password/

# Or symlink for development
ln -sf "$(pwd)" ~/.openclaw/extensions/1password
```

### 4.3 Enable in config

Add to `~/.openclaw/openclaw.json`:

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

### 4.4 Test

```bash
openclaw op-secrets test
# Expected: "1Password connection OK — 1 vault(s): Agent Secrets (id)"

openclaw op-secrets read "OpenAI API"
# Expected: "Agent Secrets/OpenAI API/api key: sk-pro...[154 chars]...EEwA"
```

---

## Step 5: Publish to npm

### 5.1 Ensure build is fresh

```bash
npm run build
```

### 5.2 Verify package contents

```bash
npm pack --dry-run
```

Should show: `dist/`, `skills/`, `openclaw.plugin.json`, `package.json`, `README.md`

### 5.3 Publish

```bash
npm publish --access public
```

### 5.4 Verify installation

```bash
openclaw plugins install @wipcomputer/wip-1password
openclaw op-secrets test
```

---

## File Inventory

After completing all steps, the project should contain:

```
openclaw-1password/
├── .gitignore
├── package.json              # npm metadata, scripts, openclaw.extensions
├── tsconfig.json             # TypeScript config
├── openclaw.plugin.json      # OpenClaw plugin manifest
├── README.md                 # User-facing docs
├── LICENSE                   # MIT
├── docs/
│   ├── PRD.md                # Product requirements
│   └── DEVELOPMENT.md        # This file
├── src/
│   └── index.ts              # Plugin code (~480 lines)
├── skills/
│   └── op-secrets/
│       └── SKILL.md          # Agent-facing skill documentation
└── dist/                     # Built output (git-ignored)
    ├── index.js
    └── index.d.ts
```

---

## Key API Reference

### 1Password SDK

```typescript
import { createClient } from "@1password/sdk";

const client = await createClient({
  auth: "ops_...",
  integrationName: "OpenClaw",
  integrationVersion: "0.1.0",
});

// Resolve a secret by reference
const value = await client.secrets.resolve("op://Vault Name/Item Title/field name");

// List vaults
const vaults = await client.vaults.list();
// Returns: [{ id: string, title: string, createdAt: string, updatedAt: string }]

// List items in a vault
const items = await client.items.list(vaultId);
// Returns: [{ id: string, title: string, category: string, ... }]
```

### OpenClaw Plugin SDK

```typescript
import type { OpenClawPluginApi } from "openclaw/plugin-sdk";

// Register an agent tool
api.registerTool(
  {
    name: "tool_name",
    description: "What it does",
    parameters: { type: "object", properties: { ... }, required: [...] },
    async execute(_id, params) {
      return { content: [{ type: "text", text: "result" }] };
    },
  },
  { optional: true },
);

// Register CLI commands
api.registerCli(
  ({ program }) => {
    program.command("my-cmd").description("...").action(async () => { ... });
  },
  { commands: ["my-cmd"] },
);

// Access plugin config
const cfg = (api.config as any)?.plugins?.entries?.["plugin-id"]?.config;
```
