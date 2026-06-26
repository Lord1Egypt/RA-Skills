# Bug: Hardcoded paths across all plugins and extensions

**Date:** 2026-03-30
**Filed by:** cc-mini
**Priority:** critical

## Problem

Multiple plugins and extensions have paths hardcoded to `~/Documents/wipcomputer--mac-mini-01/staff/...`. The workspace moved to `~/wipcomputerinc/` on Mar 24. Six days later, we're still finding broken references. This isn't a one-off fix. It's a systematic failure: no audit was done during migration, and the config-dependencies system wasn't used.

## Every hardcoded reference found

### Deployed extensions (live, affecting production)

| Plugin | File | Line | Hardcoded path |
|--------|------|------|---------------|
| memory-crystal | `~/.openclaw/extensions/memory-crystal/dist/openclaw.js` | 16 | `STAFF_DIR = ~/Documents/wipcomputer--mac-mini-01/staff` |
| memory-crystal | `~/.ldm/extensions/memory-crystal/dist/openclaw.js` | 16 | Same |
| session-export | `~/.openclaw/extensions/session-export/dist/index.js` | 7 | `DEFAULT_OUTPUT_DIR = ~/Documents/.../Lēsa/documents/sessions` |
| session-export | `~/.ldm/extensions/session-export/dist/index.js` | 7 | Same |
| private-mode | `~/.openclaw/extensions/private-mode/dist/openclaw.js` | 779-780 | Lesa + Parker dev-updates paths |
| private-mode | `~/.ldm/extensions/private-mode/dist/openclaw.js` | 779-780 | Same |
| cc-session-export | `~/.ldm/extensions/cc-session-export/dist/index.js` | 7 | Lesa sessions path |
| cc-session-export | `~/.ldm/extensions/cc-session-export/export-session.js` | 17 | Parker CC sessions path |
| cc-session-export | `~/.ldm/extensions/cc-session-export/cc-export-hook.js` | 12 | Parker CC sessions path |

### Config files (already fixed Mar 30)

| File | What was wrong | Status |
|------|---------------|--------|
| `~/.ldm/config.json` | `paths.icloud` pointed to old path | FIXED: removed |
| `~/.ldm/config-from-home.json` | Same | FIXED: removed |
| `~/.claude/CLAUDE.md` | Screenshot fallback path | FIXED: removed |
| `~/.openclaw/wip-healthcheck/config.json` | Was already clean | OK |

## The fix: all plugins read from config

Every plugin that needs workspace paths must read from `~/.ldm/config.json`:

```javascript
function resolveWorkspace() {
  const configPath = join(process.env.HOME || '~', '.ldm', 'config.json');
  if (existsSync(configPath)) {
    try {
      const config = JSON.parse(readFileSync(configPath, 'utf8'));
      if (config.workspace) return config.workspace;
    } catch {}
  }
  return join(process.env.HOME || '~', 'wipcomputerinc');
}
```

Paths derived from workspace:
- Team documents: `join(workspace, 'team/Lēsa/documents/...')`
- CC documents: `join(workspace, 'team/cc-mini/documents/...')`
- Repos: `join(workspace, 'repos/...')`

No hardcoded workspace paths. Ever. The config is the single source of truth.

## Repos to fix

| Repo | Location | What to fix |
|------|----------|-------------|
| memory-crystal-private | `repos/ldm-os/components/memory-crystal-private/` | STAFF_DIR in OpenClaw plugin |
| wip-private-mode-private | `repos/ldm-os/utilities/wip-private-mode-private/` | dev-updates paths in plugin |
| session-export | Check if standalone or in wip-ldm-os-private | DEFAULT_OUTPUT_DIR |
| cc-session-export | `repos/ldm-os/components/cc-session-export/` or in team | Three files with old paths |

## Prevention

1. **config-dependencies.json** should be run during any migration. It tracks what files reference what paths. This system exists but wasn't used on Mar 24.

2. **`ldm doctor` path audit.** Add a check that scans all deployed extensions for paths that don't exist on disk. Flag them.

3. **No hardcoded workspace paths in any plugin.** Review rule: if a PR adds a path that starts with `~/Documents/` or any absolute workspace path, block it. Use `resolveWorkspace()` instead.

4. **Migration checklist.** When workspace paths change, run:
   ```bash
   grep -rn "OLD_PATH" ~/.openclaw/extensions/ ~/.ldm/extensions/ ~/.ldm/bin/ --include="*.js" --include="*.mjs" --include="*.sh"
   ```
   Fix everything that shows up before calling the migration done.

## Timeline

- **Mar 24:** Workspace migrated. No path audit done.
- **Mar 27:** Healthcheck plist found pointing to old path (LaunchAgents bug).
- **Mar 29:** Backup script found reading from old config path.
- **Mar 30:** Session exports discovered going to old path (6 days of silent failure). Three more plugins found with hardcoded paths. Full audit done. This bug filed.

This should never happen again.
