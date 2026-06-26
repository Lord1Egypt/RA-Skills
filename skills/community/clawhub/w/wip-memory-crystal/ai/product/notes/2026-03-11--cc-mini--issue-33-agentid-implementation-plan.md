# Issue #33: Installer should set agentId, hooks should read from LDM config

Date: 2026-03-11
Author: Claude Code (cc-mini)
Issue: https://github.com/wipcomputer/memory-crystal-private/issues/33

## Problem

The agent_id used when ingesting conversations is hardcoded in two places:

- `ldm.ts:16` ... `getAgentId()` returns `process.env.CRYSTAL_AGENT_ID || 'cc-mini'`
- `cc-hook.ts:31` ... calls `getAgentId()` which falls back to `'cc-mini'`
- `openclaw.ts:253` ... uses `ctx.agentId || 'main'`

This caused ID drift. The same agent got recorded under multiple IDs, and we had to manually merge 141K+ chunks in the database.

## Current State

`~/.ldm/agents/cc-mini/config.json`:
```json
{
  "agent": "cc",
  "harness": "claude-code-cli",
  "model": "claude-opus-4-6",
  "created": "2026-02-18",
  "memoryPaths": { ... },
  "dreamWeaver": { ... }
}
```
No `agentId` field. No config.json at all for `oc-lesa-mini`.

## Implementation Plan

### Step 1: Add `agentId` to agent config schema

**File:** `src/ldm.ts`

Add `agentId` field to the agent config. Create a new interface and read/write functions:

```typescript
interface AgentConfig {
  agentId: string;
  agent: string;
  harness: string;
  model: string;
  created: string;
  memoryPaths?: Record<string, string>;
  dreamWeaver?: Record<string, unknown>;
}

function loadAgentConfig(agentId: string): AgentConfig | null {
  const configPath = join(LDM_ROOT, 'agents', agentId, 'config.json');
  try {
    if (existsSync(configPath)) {
      return JSON.parse(readFileSync(configPath, 'utf-8'));
    }
  } catch {}
  return null;
}
```

### Step 2: Update `getAgentId()` to read from config

**File:** `src/ldm.ts`

Change the resolution order:
1. `CRYSTAL_AGENT_ID` env var (explicit override)
2. Read from `~/.ldm/agents/*/config.json` (auto-detect which agent dir has a config with matching harness)
3. Detect harness type: if running inside Claude Code hook, use `cc-mini`; if OpenClaw, use `oc-lesa-mini`
4. Fall back to `'cc-mini'` only as last resort

Simpler approach: since cc-hook always runs as Claude Code and openclaw.ts always runs as OpenClaw, the caller already knows who it is. Pass the agentId explicitly rather than auto-detecting.

**Recommended:** Make `getAgentId()` smarter but keep it simple:

```typescript
export function getAgentId(harnessHint?: 'claude-code' | 'openclaw'): string {
  // 1. Explicit env var always wins
  if (process.env.CRYSTAL_AGENT_ID) return process.env.CRYSTAL_AGENT_ID;

  // 2. Check agent configs for matching harness
  const agentsDir = join(LDM_ROOT, 'agents');
  if (existsSync(agentsDir)) {
    for (const dir of readdirSync(agentsDir)) {
      const cfgPath = join(agentsDir, dir, 'config.json');
      try {
        const cfg = JSON.parse(readFileSync(cfgPath, 'utf-8'));
        if (cfg.agentId) {
          if (!harnessHint) return cfg.agentId; // first match
          if (harnessHint === 'claude-code' && cfg.harness === 'claude-code-cli') return cfg.agentId;
          if (harnessHint === 'openclaw' && cfg.harness === 'openclaw') return cfg.agentId;
        }
      } catch {}
    }
  }

  // 3. Fallback
  return harnessHint === 'openclaw' ? 'oc-lesa-mini' : 'cc-mini';
}
```

### Step 3: Update cc-hook.ts

**File:** `src/cc-hook.ts`, line 31

Change:
```typescript
const CC_AGENT_ID = process.env.CRYSTAL_AGENT_ID || 'cc-mini';
```

To:
```typescript
const CC_AGENT_ID = getAgentId('claude-code');
```

### Step 4: Update openclaw.ts

**File:** `src/openclaw.ts`

Where `ctx.agentId || 'main'` appears, change to:
```typescript
ctx.agentId || getAgentId('openclaw')
```

### Step 5: Installer asks for agent name

**File:** `src/installer.ts`

During `crystal init`, after scaffolding LDM:

1. Detect the harness type (Claude Code CLI vs OpenClaw)
2. Prompt for agent name or auto-generate using convention: `[platform]-[agent]-[machine]`
3. Write `agentId` to the agent's `config.json`
4. If `config.json` already exists but has no `agentId`, add it (migration)

```typescript
// In runInstallOrUpdate(), after scaffoldLdm():
const agentConfig = loadAgentConfig(agentId);
if (agentConfig && !agentConfig.agentId) {
  agentConfig.agentId = agentId;
  saveAgentConfig(agentId, agentConfig);
  log(`  Added agentId "${agentId}" to config.json`);
}
```

### Step 6: Create oc-lesa-mini config.json

**File:** `src/installer.ts` (when OC is detected)

If `~/.ldm/agents/oc-lesa-mini/` exists but has no `config.json`, create one:

```json
{
  "agentId": "oc-lesa-mini",
  "agent": "lesa",
  "harness": "openclaw",
  "model": "claude-sonnet-4-6",
  "created": "2026-02-09"
}
```

### Step 7: Migration for existing installs

Add a `migrateAgentConfigs()` function called during `crystal init` and `crystal doctor`:

1. Scan `~/.ldm/agents/*/config.json`
2. Any config missing `agentId` gets it added (using the directory name as the value)
3. Report what was migrated

## Files Changed

| File | Change |
|------|--------|
| `src/ldm.ts` | `AgentConfig` interface, `loadAgentConfig()`, `saveAgentConfig()`, updated `getAgentId()` |
| `src/cc-hook.ts` | Use `getAgentId('claude-code')` instead of hardcoded fallback |
| `src/openclaw.ts` | Use `getAgentId('openclaw')` instead of `'main'` fallback |
| `src/installer.ts` | Write `agentId` to config during install, create oc-lesa-mini config |
| `src/doctor.ts` | Check for missing `agentId`, offer to fix |

## Naming Convention

Format: `[platform]-[agent]-[machine]`
- `cc-mini` = Claude Code on Mac mini
- `cc-air` = Claude Code on MacBook Air
- `oc-lesa-mini` = OpenClaw Lesa on Mac mini

## Risk

Low. All changes are additive:
- Existing env var override still works
- Hardcoded fallbacks remain as last resort
- Config migration is non-destructive (adds field, doesn't change existing)
- No database schema changes
