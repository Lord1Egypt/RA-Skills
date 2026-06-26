# Troubleshooting Guide: Why CLI Commands Didn't Work (And How We Fixed Them)

## Problem

After installing `openclaw-session-compact` from ClawHub, the CLI commands (`openclaw compact`, `openclaw compact-status`, `openclaw compact-config`) were not recognized. The skill didn't even appear in `openclaw skills list`.

---

## Root Cause Analysis

### Issue 1: SKILL.md Missing YAML Frontmatter

OpenClaw's workspace skill scanner requires every `SKILL.md` to start with YAML frontmatter containing `name` and `description` fields:

```yaml
---
name: openclaw-session-compact
description: |
  Intelligent session compression plugin for OpenClaw...
---
```

**What happened**: Our `SKILL.md` started directly with `# OpenClaw Session Compact Skill 🔄` — no frontmatter. The `loadSingleSkillDirectory()` function in OpenClaw's source code parses the frontmatter and returns `null` if `name` or `description` is missing, causing the skill to be **silently skipped** during discovery.

**How we found it**: We read OpenClaw's source code at `/opt/homebrew/lib/node_modules/openclaw/dist/skills-BnlzYY40.js` and found:
```javascript
const name = frontmatter.name?.trim() || fallbackName;
const description = frontmatter.description?.trim();
if (!name || !description) return null;  // ← silently skipped!
```

### Issue 2: Wrong Extension System

OpenClaw has **two separate extension systems** that serve completely different purposes:

| Aspect | Workspace Skill | Plugin |
|--------|----------------|--------|
| **Location** | `workspace/skills/` | `~/.openclaw/extensions/` |
| **Purpose** | Documentation for LLM prompts | Executable code |
| **Entry Point** | `SKILL.md` with frontmatter | `dist/index.js` with `register()` |
| **CLI Commands** | ❌ Not supported | ✅ Supported via `api.registerCli()` |
| **Code Execution** | ❌ No | ✅ Yes |

**What happened**: Our project was structured as an npm package (with `dist/index.js`, `package.json`, `node_modules/`) but installed into `workspace/skills/`. OpenClaw loaded the `SKILL.md` as documentation only — the compiled JavaScript was never executed.

**How we found it**: We compared working skills:
- `acpx-qwen`, `skill-vetter` — simple directories with just `SKILL.md` (no `package.json`)
- `feishu-bitable` — has `package.json` but loaded as `openclaw-extra` source, not `openclaw-workspace`

### Issue 3: Wrong Key in package.json

```json
// ❌ What we had
"openclaw": {
  "entry": "dist/index.js"
}

// ✅ What OpenClaw plugin discovery requires
"openclaw": {
  "extensions": ["./dist/index.js"]
}
```

**What happened**: OpenClaw's plugin discovery (`resolvePackageExtensionEntries` in `manifest-BLZdOZfM.js`) looks for `manifest.openclaw.extensions` array. The `"entry"` key was ignored, so no extension entries were found.

### Issue 4: Missing openclaw.plugin.json

Plugins require a manifest file `openclaw.plugin.json`:

```json
{
  "id": "openclaw-session-compact",
  "cli": ["compact", "compact-status", "compact-config"],
  "configSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {}
  }
}
```

**What happened**: Without this file, plugin loading failed with:
```
Invalid config: plugin manifest requires configSchema
```

### Issue 5: Wrong Export Format in src/index.ts

```typescript
// ❌ Initial format — OpenClaw doesn't recognize this
export const skill = {
  name: 'session-compact',
  cli: {
    register: (program: Command) => { ... }
  }
};

// ✅ Correct plugin entry point
export function register(api: any) {
  api.registerCli(
    async ({ program }) => {
      program.command('compact').action(...)
      program.command('compact-status').action(...)
      program.command('compact-config').action(...)
    },
    {
      commands: ['compact', 'compact-status', 'compact-config'],
      descriptors: [
        { name: 'compact', description: '...' },
        ...
      ]
    }
  );
}
```

**What happened**: Without a proper `register` export, OpenClaw logged:
```
[plugins] openclaw-session-compact missing register/activate export
```

### Issue 6: Plugin Not in Allowlist

OpenClaw requires plugins to be explicitly allowed in `openclaw.json`:

```json
{
  "plugins": {
    "allow": ["openclaw-session-compact"],
    "entries": {
      "openclaw-session-compact": { "enabled": true }
    }
  }
}
```

**What happened**: Without this, CLI commands failed with:
```
The `openclaw compact` command is unavailable because `plugins.allow` excludes "compact".
```

---

## How We Fixed It (Step by Step)

### Step 1: Add YAML Frontmatter to SKILL.md

```markdown
---
name: openclaw-session-compact
description: |
  Intelligent session compression plugin for OpenClaw that automatically
  manages token consumption and supports unlimited-length conversations.
---

# OpenClaw Session Compact Plugin
...
```

**Result**: Skill now appears in `openclaw skills list` as `✓ ready`.

### Step 2: Create openclaw.plugin.json

```json
{
  "id": "openclaw-session-compact",
  "cli": ["compact", "compact-status", "compact-config"],
  "configSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {}
  }
}
```

### Step 3: Fix package.json Key

Changed `"openclaw.entry"` to `"openclaw.extensions"`:

```json
{
  "openclaw": {
    "extensions": ["./dist/index.js"]
  }
}
```

### Step 4: Rewrite src/index.ts

Replaced the `skill` object export with a proper `register(api)` function using `api.registerCli()`.

### Step 5: Install as Plugin

Copied the built project to `~/.openclaw/extensions/openclaw-session-compact/` and ran `npm install`.

### Step 6: Update openclaw.json

Added the plugin to both `plugins.allow` and `plugins.entries`.

### Step 7: Rebuild

```bash
npm run build
```

---

## Final Result

All three CLI commands now work:

```bash
$ openclaw compact-status
📊 Session Status
────────────────────────────────────
  Current tokens: 41
  Threshold:      10,000
  Usage:          0%
  Status:         ✅ OK
────────────────────────────────────
  Preserve recent: 4 messages
  Auto compact:    Enabled
  Model:           qwen/qwen3.5-122b-a10b

$ openclaw compact
📊 Current session tokens: 41
📉 Threshold: 10000
✅ Session is within token limits. No compaction needed.

$ openclaw compact-config
🔧 Current Configuration
────────────────────────────────────
  max_tokens: 10000
  preserve_recent: 4
  auto_compact: true
  model:
```

---

## Key Takeaways

1. **SKILL.md always needs YAML frontmatter** — without `name` and `description`, skills are silently skipped
2. **Workspace skills ≠ Plugins** — skills are documentation-only; plugins execute code
3. **Plugin discovery uses `openclaw.extensions`** — not `openclaw.entry`
4. **Plugins need `openclaw.plugin.json`** — with `id`, `cli`, and `configSchema`
5. **Plugin entry point is `register(api)`** — not a `skill` object
6. **CLI registration uses `api.registerCli()`** — not `api.registerCommand()`
7. **Plugins must be in `plugins.allow`** — otherwise commands are blocked

---

## ClawHub Publishing Issues

### Issue 7: Package Name Collides with Existing Skill Slug

**Error**: `Package name collides with existing skill slug "openclaw-session-compact"`

**Cause**: We previously published as a skill (`clawhub publish`), which created a skill slug. Code plugins and skills share the same namespace.

**Solution**: Delete the old skill first, then publish as a code plugin:
```bash
clawhub delete openclaw-session-compact --yes
clawhub package publish . --family code-plugin --source-repo ... --source-commit ... --version 1.0.0
```

### Issue 8: Missing `openclaw.compat.pluginApi`

**Error**: `package.json openclaw.compat.pluginApi is required`

**Cause**: ClawHub code plugins require compatibility metadata.

**Solution**: Add to `package.json`:
```json
{
  "openclaw": {
    "compat": {
      "pluginApi": ">=2026.4.2"
    }
  }
}
```

### Issue 9: Missing `openclaw.build.openclawVersion`

**Error**: `package.json openclaw.build.openclawVersion is required`

**Cause**: ClawHub needs to know which OpenClaw version the plugin was built with.

**Solution**: Add to `package.json`:
```json
{
  "openclaw": {
    "build": {
      "openclawVersion": "2026.4.5"
    }
  }
}
```

### Issue 10: `clawhub install` Doesn't Support Code Plugins Yet

**Error**: `Skill not found` when running `clawhub install openclaw-session-compact`

**Cause**: `clawhub install` is designed for skills (SKILL.md), not code plugins. Code plugins need manual installation.

**Solution**: Manual installation:
```bash
git clone https://github.com/SDC-creator/openclaw-session-compact.git \
  ~/.openclaw/extensions/openclaw-session-compact
cd ~/.openclaw/extensions/openclaw-session-compact
npm install --production
```

---

*Document created: 2026-04-06*
*Last updated: 2026-04-07*
*OpenClaw version: 2026.4.5*
*ClawHub CLI version: 0.9.0*
