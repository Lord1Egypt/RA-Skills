# Plan: Install Everything, Enable/Disable What You Use

## Context

During Air dogfood, `ldm install` shows 8 catalog items and asks the user to pick. Parker's insight: just install everything. Memory Crystal is the OS's memory layer, not optional. Everything else installs but stays off until you turn it on. Like iOS: every app is on the phone, you activate what you want.

Issue: #111

## Architecture

### Two states per extension

Currently: installed = active. No distinction.

New: every extension has two states in registry.json:
- **installed**: files exist in `~/.ldm/extensions/`
- **enabled**: interfaces are active (MCP registered, hooks wired, skills deployed)

```json
{
  "memory-crystal": {
    "name": "memory-crystal",
    "version": "0.7.28",
    "enabled": true,
    "interfaces": ["cli", "module", "mcp", "openclaw"],
    ...
  },
  "wip-xai-grok": {
    "name": "wip-xai-grok",
    "version": "1.0.3",
    "enabled": false,
    "interfaces": ["cli", "module", "mcp", "skill"],
    ...
  }
}
```

### What "enabled" controls

| Interface | Enabled | Disabled |
|-----------|---------|----------|
| CLI | On PATH | On PATH (always, needed for `ldm enable`) |
| MCP | Registered in ~/.claude.json | Unregistered |
| CC Hook | In ~/.claude/settings.json | Removed from settings |
| Skill | In ~/.openclaw/skills/ | Removed |
| OpenClaw plugin | In openclaw.json extensions | Removed from extensions |
| Module | Importable | Importable (always, library code) |

CLIs and modules stay available always. MCP servers, hooks, and skills get toggled.

### Tiers

**Core (always installed, always enabled, no prompt):**
- LDM OS CLI
- Memory Crystal (+ `crystal init` runs as postInstall)

**Optional (installed, disabled by default, user enables):**
- AI DevOps Toolbox
- 1Password
- Markdown Viewer
- xAI Grok
- X Platform
- Dream Weaver Protocol

**Stacks (groups for enabling):**
- `ldm enable core` ... enables Memory Crystal (already on) + DevOps Toolbox + 1Password + Markdown Viewer
- `ldm enable web` ... enables Playwright + next-devtools + shadcn + tailwindcss-docs MCP servers
- `ldm enable all` ... enables everything

### New commands

```bash
ldm enable <name|stack>     # Register MCP, wire hooks, deploy skills
ldm disable <name|stack>    # Unregister MCP, remove hooks, remove skills
ldm status                  # Shows installed + enabled/disabled state
```

### Fresh install flow

```bash
ldm install   # on fresh machine

1. Self-update CLI if behind
2. ldm init (scaffold ~/.ldm/)
3. Install ALL catalog components (no prompt)
4. Auto-enable core: Memory Crystal + crystal init
5. Show what's installed and what's enabled:

  Installed (8 extensions):

  Enabled:
    [*] Memory Crystal    v0.7.28   (Core, always on)

  Disabled (enable when ready):
    [ ] AI DevOps Toolbox v1.9.44   ldm enable devops-toolbox
    [ ] 1Password         v0.2.2    ldm enable 1password
    [ ] Markdown Viewer   v1.2.6    ldm enable markdown-viewer
    [ ] xAI Grok          v1.0.3    ldm enable grok
    [ ] X Platform        v1.0.4    ldm enable x
    [ ] Dream Weaver      v1.0.0    ldm enable dream-weaver

6. Done. One command. Everything installed. Core active. Rest waiting.
```

## Implementation

### Phase 1: Add `enabled` field to registry

**File:** `wip-ldm-os-private/lib/deploy.mjs`

In `updateRegistry()`, add `enabled` field. Default to `true` for core (memory-crystal), `false` for everything else.

```javascript
function updateRegistry(name, info) {
  const registry = loadRegistry();
  const isCore = name === 'memory-crystal';
  registry.extensions[name] = {
    ...registry.extensions[name],
    ...info,
    enabled: registry.extensions[name]?.enabled ?? isCore,
    updatedAt: new Date().toISOString(),
  };
  saveRegistry(registry);
}
```

### Phase 2: Conditional interface deployment

**File:** `wip-ldm-os-private/lib/deploy.mjs`

In `installSingleTool()`, check `enabled` before deploying MCP, hooks, and skills:

```javascript
const isEnabled = registry.extensions[toolName]?.enabled ?? true;

if (interfaces.mcp && isEnabled) {
  registerMCP(toolPath, interfaces.mcp, toolName);
}
if (interfaces.claudeCodeHook && isEnabled) {
  installClaudeCodeHook(toolPath, interfaces.claudeCodeHook);
}
if (interfaces.skill && isEnabled) {
  installSkill(toolPath, toolName);
}
```

Files are always deployed to `~/.ldm/extensions/`. Only interface registrations are conditional.

### Phase 3: `ldm enable` / `ldm disable` commands

**File:** `wip-ldm-os-private/bin/ldm.js`

New commands that toggle the `enabled` flag and rebuild interface registrations:

```javascript
async function cmdEnable(target) {
  // target can be extension name or stack name
  const names = resolveTarget(target); // stack -> component list

  for (const name of names) {
    const entry = registry.extensions[name];
    if (!entry) { console.log(`  ${name}: not installed`); continue; }
    if (entry.enabled) { console.log(`  ${name}: already enabled`); continue; }

    // Register interfaces
    const extPath = entry.ldmPath;
    const { interfaces } = detectInterfaces(extPath);
    if (interfaces.mcp) registerMCP(extPath, interfaces.mcp, name);
    if (interfaces.claudeCodeHook) installClaudeCodeHook(extPath, interfaces.claudeCodeHook);
    if (interfaces.skill) installSkill(extPath, name);

    // Run postInstall if defined
    const catalogEntry = findInCatalog(name);
    if (catalogEntry?.postInstall) {
      execSync(catalogEntry.postInstall, { stdio: 'inherit' });
    }

    // Update registry
    entry.enabled = true;
    saveRegistry(registry);
    console.log(`  + ${name} enabled`);
  }
}

async function cmdDisable(target) {
  const names = resolveTarget(target);

  for (const name of names) {
    if (name === 'memory-crystal') {
      console.log('  ! Memory Crystal is core. Cannot disable.');
      continue;
    }

    const entry = registry.extensions[name];
    if (!entry?.enabled) { continue; }

    // Unregister interfaces
    unregisterMCP(name);
    removeClaudeCodeHook(name);
    removeSkill(name);

    entry.enabled = false;
    saveRegistry(registry);
    console.log(`  - ${name} disabled`);
  }
}
```

### Phase 4: Fresh install installs everything

**File:** `wip-ldm-os-private/bin/ldm.js`, in `cmdInstallCatalog()`

On fresh install (no extensions registered), skip the interactive prompt. Install all catalog components. Enable only core.

```javascript
if (totalExtensions === 0 && !DRY_RUN) {
  console.log('  Fresh install. Installing all components...');
  for (const comp of components) {
    if (comp.status === 'coming-soon') continue;
    console.log(`  Installing ${comp.name}...`);
    execSync(`ldm install ${comp.repo}`, { stdio: 'inherit' });
  }
  // Memory Crystal is auto-enabled by updateRegistry (isCore check)
  // Everything else is disabled by default
  console.log('');
  console.log('  Core enabled: Memory Crystal');
  console.log('  Run "ldm enable <name>" to activate other tools.');
}
```

### Phase 5: New unregister functions

**File:** `wip-ldm-os-private/lib/deploy.mjs`

New functions to undo interface registrations:

```javascript
function unregisterMCP(name) {
  // Remove from ~/.claude.json mcpServers
  // claude mcp remove --scope user <name>
}

function removeClaudeCodeHook(name) {
  // Remove hook entries from ~/.claude/settings.json
  // Match by command path containing the extension name
}

function removeSkill(name) {
  // rm -rf ~/.openclaw/skills/<name>/
}
```

### Phase 6: Update `ldm status`

Show enabled/disabled state:

```
  LDM OS v0.4.28 (latest)

  Enabled:
    [*] Memory Crystal    v0.7.28   Core
    [*] DevOps Toolbox    v1.9.44

  Disabled:
    [ ] 1Password         v0.2.2    ldm enable 1password
    [ ] Grok              v1.0.3    ldm enable grok
    [ ] X Platform        v1.0.4    ldm enable x
```

## Files to modify

| File | Changes |
|------|---------|
| `lib/deploy.mjs` | Add `enabled` to registry, conditional interface deploy, unregister functions |
| `bin/ldm.js` | New enable/disable commands, fresh install logic, updated status display |
| `lib/state.mjs` | Include `enabled` in reconciliation |
| `catalog.json` | Add `core: true` field to memory-crystal (optional, could hardcode) |

## What does NOT change

- Extension file deployment (always to ~/.ldm/extensions/)
- CLI binaries (always available)
- Module imports (always available)
- Database, secrets, agent files (never touched)
- The update flow (ldm install updates all installed extensions regardless of enabled)

## Verification

```bash
# Fresh install
ldm install
# Should install all 8 extensions, enable only Memory Crystal

ldm status
# Memory Crystal: enabled. Everything else: disabled.

ldm enable devops-toolbox
# Registers MCP servers, wires hooks, deploys skills

ldm disable grok
# Unregisters MCP, removes skill

ldm enable all
# Everything active

ldm disable all
# Error: cannot disable Memory Crystal. Everything else disabled.
```
