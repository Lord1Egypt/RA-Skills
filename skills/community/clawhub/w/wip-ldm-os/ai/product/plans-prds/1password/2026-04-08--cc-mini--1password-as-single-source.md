# Plan: 1Password as Single Source of Truth for All Secrets

**Date:** 2026-04-08
**Author:** cc-mini (with Parker)
**Status:** plan approved, building next
**Repo:** `wip-1password-private` (source), all repos (consumers)

## The Problem

Every tool that needs a secret has its own broken pattern:
- `wip-xai-grok`: calls `op read` bare (no SA token), wrong item name, wrong field name, error message tells agents to `export` keys as env vars
- `wip-xai-x`: calls `op read` bare (no SA token)
- `wip-x-xai-grok` (combined, building now): needs correct pattern from day one
- Any future tool: will copy whatever pattern it finds, perpetuating the problem

The 1Password plugin (`wip-1password-private`) already does it right: JS SDK, SA token from `~/.openclaw/secrets/op-sa-token`, never shells out to `op`, never exports secrets. But no other tool uses it.

**The incident:** CC pasted an API key into a Bash `export` command during a session because the error message told it to. The key was exposed in conversation context. This is the direct consequence of tools rolling their own secret access instead of using the central system.

## The Solution

**One package handles all secret access.** Every tool imports from `@wipcomputer/wip-1password` instead of writing its own `op` calls.

## What Exists Today (correct)

`wip-1password-private/src/index.ts`:
- `@1password/sdk` JS SDK (headless, no desktop app)
- SA token from `~/.openclaw/secrets/op-sa-token` (never bare `op`)
- `resolveSecret(vault, item, field)` ... reads any secret
- `resolveSecretRefs(obj)` ... walks a config object, resolves `op://` references
- `op_read_secret` tool ... agents can read secrets
- `op_list_items` tool ... agents can list vault contents
- `op_write_secret` tool ... agents can store secrets
- Startup service that resolves `op://` refs in config + sets `OPENAI_API_KEY`

## What Needs to Change

### Phase 1: Export a helper function from wip-1password

**File:** `wip-1password-private/src/helper.ts` (new)

```typescript
export async function opRead(
  item: string,
  field?: string,
  vault?: string,
): Promise<string>
```

This is a standalone function that:
- Creates its own SDK client (lazy singleton, same as plugin)
- Reads the SA token from `~/.openclaw/secrets/op-sa-token`
- Resolves the secret via SDK (not CLI)
- Returns the value
- Throws with a clear error (no "export" suggestions)

**Package.json exports:**
```json
{
  "exports": {
    ".": "./dist/index.js",
    "./helper": "./dist/helper.js"
  }
}
```

Other tools import:
```javascript
import { opRead } from '@wipcomputer/wip-1password/helper';
const key = await opRead('x.ai - wip-computer-beta', 'credential');
```

### Phase 2: Update all tools to use the helper

Every tool that touches 1Password needs to be updated:

| Tool | Current pattern | Fix |
|---|---|---|
| `wip-x-xai-grok` (combined, building now) | New code | Use helper from day one |
| `wip-xai-grok-private-deprecated` | `execSync('op read ...')` bare | Deprecated, no fix needed |
| `wip-xai-x-private-deprecated` | `execSync('op read ...')` bare | Deprecated, no fix needed |
| `wip-healthcheck` | Unknown, check | Update if needed |
| Any future MCP server/tool | N/A | Must use helper, enforced by convention |

### Phase 3: Fix error messages everywhere

Every error message that suggests `export XYZ_API_KEY=` must be changed to:
- "Add the secret to 1Password: vault 'Agent Secrets', item 'Name', field 'field'"
- "Or check your SA token at ~/.openclaw/secrets/op-sa-token"
- Never suggest environment variable export

### Phase 4: Update documentation

| Document | What to update |
|---|---|
| `wip-1password-private/README.md` | Add "For tool developers" section with import examples |
| `wip-1password-private/TECHNICAL.md` | Document the helper export, SDK client lifecycle |
| `~/wipcomputerinc/CLAUDE.md` | Already has the SA token rule. Add: "All tools must use @wipcomputer/wip-1password/helper for secrets. Never shell out to op." |
| `~/wipcomputerinc/settings/docs/system-directories.md` | Document `~/.openclaw/secrets/op-sa-token` location |
| `~/.ldm/agents/cc-mini/CONTEXT.md` or equivalent | Add rule about never exporting secrets |
| `wip-ldm-os-private/CLAUDE.md` | Add rule: "All MCP servers and tools must import secret access from @wipcomputer/wip-1password/helper. Never call op directly. Never suggest export of API keys." |
| Each tool's SKILL.md | Remove any "set XYZ_API_KEY" instructions |

### Phase 5: 1Password item audit

Verify all items in "Agent Secrets" vault have consistent naming:

| Current item name | Used by | Field |
|---|---|---|
| x.ai - wip-computer-beta | wip-x-xai-grok (Grok API) | credential |
| X API Key - wip-01 | wip-x-xai-grok (X Platform) | bearer token, api key, api secret, access token, access token secret |
| OpenAI API | 1password plugin (startup service) | api key |
| Postgres VPS (kaleidoscope) | server.mjs (manual) | password |
| Service Account Auth Token: OpenClaw Agent | SA token file | token |
| npm Token | wip-release | (check field) |
| Tavily API | tavily plugin | api key |
| Anthropic Auth Token - * | openclaw auth profiles | api key |

Each tool must reference the correct item name and field name. Mismatches (like wip-xai-grok looking for "X API" when the item is "x.ai - wip-computer-beta") are the #1 cause of tools falling back to broken patterns.

## Implementation Order

1. Add `helper.ts` to `wip-1password-private` with standalone `opRead`
2. Build + publish new version
3. Update `wip-x-xai-grok-private` (combined) to use helper (being built now)
4. Update CLAUDE.md files with the new rule
5. Update README/TECHNICAL docs in wip-1password-private
6. Audit all 1Password items for naming consistency
7. Update deployed extensions via `ldm install`

## The Rule (add to CLAUDE.md)

```
## Secret Access: One Way Only

All tools, MCP servers, and extensions MUST use @wipcomputer/wip-1password/helper 
for secret access. Import opRead, pass the item name and field.

NEVER:
- Call `op` or `op read` directly (bare or with SA token prefix)
- Suggest `export API_KEY=` in error messages
- Hardcode secrets in source code
- Read secrets from environment variables as primary path

The 1Password JS SDK handles everything. The SA token lives at 
~/.openclaw/secrets/op-sa-token. The helper reads it automatically.
```

## Cross-references

- `repos/ldm-os/utilities/wip-1password-private/` ... the plugin source
- `~/.openclaw/extensions/wip-1password/` ... deployed plugin
- `~/.openclaw/secrets/op-sa-token` ... SA token (never in git)
- `ai/product/plans-prds/kaleidoscope/2026-04-07--cc-mini--features-to-preserve-from-demo.md` ... auth SDK idea
- Incident: CC exported xAI API key in Bash during session (2026-04-08)
