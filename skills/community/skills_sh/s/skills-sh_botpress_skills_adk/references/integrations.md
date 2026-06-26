# Integration Management

Integrations connect your agent to external platforms and services. Manage them through the CLI or Dev Console — never hand-edit dependency snapshots.

## CLI Commands

All integration management uses the `adk integrations` subcommand family. Every mutation command supports `--target <env>` (dev or prod, default: dev) and `--format <format>` (text or json).

> **Removed aliases:** The old flat commands (`adk add`, `adk remove`, `adk search`, `adk list`, `adk info`, `adk upgrade`) are no longer part of the public CLI. Use the `adk integrations` subcommands instead.

### Discovery

| Command                                      | Description                                       | Key Flags                    |
| -------------------------------------------- | ------------------------------------------------- | ---------------------------- |
| `adk integrations search <query>`            | Search Hub integrations by keyword                | `--format json`              |
| `adk integrations search --interface <name>` | Find Hub integrations that implement an interface | `--format json`              |
| `adk integrations list`                      | Show installed dependencies                       | `--format json`, `--verbose` |
| `adk integrations info <name[@version]>`     | Full integration details                          | `--format json`              |

Use `--format json` for programmatic inspection of config schemas, action shapes, and event payloads.

### Mutations

| Command                                 | Description                             | Key Flags                                                |
| --------------------------------------- | --------------------------------------- | -------------------------------------------------------- |
| `adk integrations add <name>@<version>` | Install an integration                  | `--alias <name>`, `--target <env>`, `--config key=value` |
| `adk integrations remove <alias>`       | Uninstall an integration                | `--target <env>`                                         |
| `adk integrations upgrade <alias>`      | Upgrade to latest (or specific) version | `--to <version>`, `--target <env>`                       |
| `adk integrations enable <alias>`       | Enable a disabled integration           | `--target <env>`                                         |
| `adk integrations disable <alias>`      | Disable without removing                | `--target <env>`                                         |
| `adk integrations configure <alias>`    | Set or unset config values              | `--set key=value`, `--unset key`, `--target <env>`       |

### State Inspection and Promotion

| Command                   | Description                                 | Key Flags                                          |
| ------------------------- | ------------------------------------------- | -------------------------------------------------- |
| `adk integrations status` | Show capability state and remediation       | `--target <env>`, `--format json`                  |
| `adk integrations copy`   | Copy integration state between environments | `--from <env>`, `--to <env>`, `--dry-run`, `--yes` |
| `adk integrations diff`   | Show snapshot vs Cloud differences          | `--target <env>`                                   |

## Snapshot System

Integration state lives in Botpress Cloud. The ADK writes generated per-environment snapshots under `.adk/dependencies/`:

- `.adk/dependencies/dev.json` — development environment snapshot
- `.adk/dependencies/prod.json` — production environment snapshot
- `.adk/dependencies/migration.json` — one-way legacy migration marker

```json
{
  "version": 1,
  "env": "dev",
  "botId": "bot_123",
  "fetchedAt": "2026-06-10T12:00:00.000Z",
  "integrations": {
    "slack": {
      "name": "slack",
      "version": "3.0.0",
      "enabled": true,
      "config": {
        "replyBehaviour": "start-conversation",
        "apiSecret": "${env:SLACK_SECRET}"
      }
    },
    "browser": {
      "name": "browser",
      "version": "0.8.6",
      "enabled": true,
      "config": {}
    }
  },
  "plugins": {}
}
```

**Key principles:**

- Cloud is the source of truth. Snapshots are local reflections refreshed after mutations and Cloud reads.
- Never edit snapshots by hand — use `adk integrations` commands or the Dev Console.
- The `--target` flag controls which environment (dev/prod) a command operates on.
- Config values support env substitution: `${env:API_KEY}` resolves to `process.env.API_KEY` at apply time.
- Use `adk dependencies export` / `adk dependencies import` for explicit dependency-only restore artifacts. These files are separate from generated `.adk/dependencies/*.json` snapshots.

**Migration from agent.config.ts / legacy lock files:** Projects with a legacy `dependencies` block in `agent.config.ts` or legacy `dependencies.<env>.lock.json` files are auto-migrated on the first CLI command. If Cloud has no dependency state for an environment, legacy state is imported to Cloud automatically, including prod. The migration is one-shot and skipped when `.adk/dependencies/migration.json` exists; the marker contents are informational and are not parsed for gating.

## Integration Lifecycle

### 1. Discover

```bash
adk integrations search slack
adk integrations search --interface hitl
adk integrations info slack --format json
```

### 2. Add

```bash
adk integrations add slack@3.0.0
adk integrations add openai@1.0.0 --alias ai
adk integrations add agi/linear@2.0.0
```

Always pin to a specific version. Without `--alias`, the integration name becomes the alias.

What happens: the integration is resolved, applied to Cloud, and the local snapshot is refreshed. OAuth or missing-required-field integrations may be installed disabled with an `unconfigured` status until configuration/authorization is complete.

### 3. Configure

```bash
adk integrations configure slack --set replyBehaviour=start-conversation
adk integrations configure slack --set apiSecret='${env:SLACK_SECRET}'
adk integrations configure slack --unset optionalField
```

For OAuth integrations, complete the authorization flow in the Botpress Dev Console (`localhost:3001` during dev).

### 4. Enable

```bash
adk integrations enable slack
```

After enabling, the integration registers with Botpress Cloud:

```
registration_pending → registered       (success)
                     → registration_failed  (error)
```

Check status with `adk integrations status`.

### 5. Use in Code

```typescript
import { actions } from '@botpress/runtime'

await actions.slack.sendMessage({ channel: '#general', text: 'Hello!' })
await actions.browser.webSearch({ query: 'Botpress ADK' })
```

The alias determines the accessor: `actions.<alias>.<actionName>()`. See **[Integration Actions](./integration-actions.md)** for the full API reference.

### 6. Remove / Upgrade

```bash
adk integrations remove slack
adk integrations upgrade slack
```

After upgrading, check for breaking changes in the new version, then re-deploy with `adk deploy`.

### Dependency Snapshot Import/Export

```bash
adk dependencies export [file] --target dev
adk dependencies export [file] --target prod --no-config
adk dependencies import <file> --dry-run
adk dependencies import <file> --target prod --yes
```

Use these commands when you need to move or restore one environment's integration/plugin state without exporting the whole project. Export includes config by default and prints a security notice; pass `--no-config` before sharing an artifact. Import applies the captured state to the selected Cloud bot, refreshes the local snapshot, and restores the previous local snapshot after `--dry-run`.

## Configuration Types

Use `adk integrations info <name> --format json` to inspect an integration's configuration schema.

### No Config

Zero configuration properties. Just enable it.

**Example:** `browser` — add, enable, done.

### Optional Config Only

Has configuration properties but none are required. Works out of the box.

**Examples:**

- `chat` — optional `encryptionKey`, `webhookUrl`, `webhookSecret`
- `webchat` — ~38 optional theming/behavior props (`primaryColor`, `fontFamily`, `allowFileUpload`, etc.)
- `webhook` — optional `secret` and `allowedOrigins`

### OAuth (Link-Based)

Default configuration includes an `identifier` with a `linkTemplateScript`. User clicks a generated URL in the Dev Console to authorize.

**Examples:** `whatsapp` (default config), `linear` (default config)

### OAuth + Required Fields

OAuth authorization plus required configuration fields.

**Example:** `slack` — requires `replyBehaviour` in addition to OAuth. Alternative configs: `manifestAppCredentials`, `refreshToken`.

### API Key / Manual

Configuration schema has required string fields, often marked `x-zui.secret: true`. User enters values in the Dev Console or via `adk integrations configure --set`.

**Examples:** `linear` (apiKey config), `whatsapp` (manual config)

### Sandbox

Testing mode using a shared Botpress account. The integration provides a sandbox configuration with a VRL script.

**Example:** `whatsapp` sandbox config (shared test phone number: +1-581-701-9840)

### Detecting Config Type from CLI

Inspect `adk integrations info <name> --format json`:

| JSON Key                   | What It Tells You                                   |
| -------------------------- | --------------------------------------------------- |
| `configuration.schema`     | Default config schema (properties, required fields) |
| `configuration.identifier` | Whether OAuth/link-based auth is used               |
| `configurations`           | Alternative configuration types (if any)            |

If `configuration.schema.properties` is empty or all optional → no manual config needed.
If `configuration.identifier.linkTemplateScript` exists → OAuth.
If `configurations` has multiple entries → multiple modes available.

## Common Integrations Quick Reference

### chat

**Config:** Optional only (none required)
**Actions:** 1 (sendEvent) | **Channels:** 1 | **Events:** 1 (custom)

Used internally by `adk chat` CLI command. Good default for basic messaging during development.

### webchat

**Config:** Optional only (~38 theming/behavior props, none required)
**Actions:** 9 (configWebchat, showWebchat, hideWebchat, etc.) | **Channels:** 1 | **Events:** 2

Embeddable web chat widget. Works out of the box.

### browser

**Config:** None (zero properties)
**Actions:** 5 (browsePages, webSearch, discoverUrls, captureScreenshot, getWebsiteLogo) | **Channels:** 0 | **Events:** 0

Most commonly used for RAG, web search, and page scraping. No configuration needed.

### slack

**Config:** OAuth + required `replyBehaviour`
**Actions:** Multiple | **Channels:** 3 (channel, dm, thread) | **Events:** 6

After adding: enable in Dev Console, set `replyBehaviour`, complete OAuth. Alternative configs: `manifestAppCredentials`, `refreshToken`.

### whatsapp

**Config:** 3 modes (OAuth, sandbox, manual)
**Actions:** Multiple | **Channels:** 1 | **Events:** Multiple

Sandbox mode is useful for quick testing without a WhatsApp Business account.

### linear

**Name:** `agi/linear` (private, workspace-scoped) | **Config:** OAuth or API key
**Actions:** Multiple | **Channels:** Multiple | **Events:** Multiple

Use full name when searching: `adk integrations info agi/linear`.

### webhook

**Config:** Optional only (none required)
**Actions:** 0 | **Channels:** 0 | **Events:** 1

Receives external HTTP webhooks. Only fires events when a payload arrives.

## Name Resolution

| Format           | Example                             | Meaning                                     |
| ---------------- | ----------------------------------- | ------------------------------------------- |
| Plain name       | `slack`                             | Official/public integration, latest version |
| `name@version`   | `slack@3.0.0`                       | Specific version                            |
| `workspace/name` | `agi/linear`                        | Private (workspace-scoped) integration      |
| `intver_<ULID>`  | `intver_01KM6EB027NRCST3M696XT0GTW` | Exact integration version ID                |

Official integrations use just the name. Private integrations are prefixed with the workspace slug and are only visible to workspace members.
