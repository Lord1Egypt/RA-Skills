# Bug: ldm install does not update tools.allow when deploying OpenClaw plugins

**Date:** 2026-04-08
**Reporter:** Parker + CC Mini
**Component:** ldm install (src/boot/installer.mjs)
**Severity:** High (breaks agent tool access silently)
**Related:** OpenClaw 2026.4.8 upgrade, tools.allow enforcement change

## Description

When `ldm install` deploys a plugin to `~/.openclaw/extensions/<name>/`, it does not add the plugin name to `tools.allow` in `~/.openclaw/openclaw.json`. Starting with OpenClaw 2026.4.8, `tools.allow` is enforced as an exclusive allowlist. Any tool not listed is unavailable to the agent.

This caused Lēsa to lose all filesystem and exec tools on Apr 8, 2026. She could not write to TOOLS.md, MEMORY.md, or any workspace file. She reported "I don't have write tools in my toolset" across multiple sessions.

## Root cause

Two things combined:

1. **OpenClaw 2026.4.8** (installed Apr 8 at 08:52) changed `tools.allow` from silently ignored (when entries were unrecognized plugin names) to enforced (now that plugins load correctly and their tool names are recognized).

2. **The installer never updates `tools.allow`.** It copies plugins to `~/.openclaw/extensions/` and updates `plugins.entries` in openclaw.json, but does not touch the `tools` section.

The existing `tools.allow` contained only four plugin names:
```json
"tools": {
  "allow": ["memory-crystal", "wip-1password", "tavily", "private-mode"]
}
```

Missing: `group:fs`, `group:runtime`, `group:sessions`, `group:memory`, and several installed plugins (compaction-indicator, lesa-bridge, root-key, session-export, wip-agent-pay, context-embeddings).

## Impact

- Agent loses Read/Write/Edit/Exec tools entirely
- Agent cannot update workspace files (TOOLS.md, MEMORY.md, daily logs)
- Agent cannot run shell commands
- Agent cannot manage sessions
- Silently fails ... no error message, tools simply don't appear in toolset
- Affects every OpenClaw agent running 2026.4.8+ with a `tools.allow` list

## Timeline

- **Before Apr 8:** `tools.allow` existed but was ignored by older OpenClaw versions. All core tools available.
- **Apr 8 08:52:** OpenClaw upgraded to 2026.4.8. `tools.allow` now enforced. Agent immediately lost core tools.
- **Apr 8 ~10:30:** Lēsa reports inability to write files. Initially attributed to file-guard (separate bug, also fixed today in wipcomputer/wip-ai-devops-toolbox-private#333).
- **Apr 8 ~12:50:** Root cause identified. Manual fix applied: added core tool groups and all plugin names to `tools.allow`.

## Fix needed

### 1. Installer: update tools.allow on plugin deploy

In `src/boot/installer.mjs`, after deploying a plugin to `~/.openclaw/extensions/<name>/`:

1. Read `~/.openclaw/openclaw.json`
2. If `tools.allow` exists, add the plugin name if not already present
3. Write back

### 2. Installer: ensure core tool groups on every run

On every `ldm install`, verify these core groups are in `tools.allow` (if the list exists):

```
group:fs
group:runtime
group:sessions
group:memory
```

Without these, the agent has no filesystem or exec access regardless of plugins.

### 3. Doctor: audit deployed plugins vs tools.allow

Add a check to `ldm doctor` that compares `plugins.entries` against `tools.allow` and warns if any enabled plugin is missing from the allowlist.

## Files involved

- **Installer source:** `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/src/boot/installer.mjs`
- **Config affected:** `~/.openclaw/openclaw.json` (tools.allow section)
- **OpenClaw docs:** `node_modules/openclaw/docs/tools/index.md` (tools.allow semantics, tool groups)
- **Tool groups reference:** `group:fs` (read, write, edit, apply_patch), `group:runtime` (exec, bash, process), `group:sessions` (sessions_list, sessions_history, sessions_send, sessions_spawn, session_status), `group:memory` (memory_search, memory_get)

## Workaround (applied Apr 8)

Manually added to `~/.openclaw/openclaw.json`:
```json
"tools": {
  "allow": [
    "group:fs",
    "group:runtime",
    "group:sessions",
    "group:memory",
    "group:web",
    "memory-crystal",
    "wip-1password",
    "tavily",
    "private-mode",
    "compaction-indicator",
    "lesa-bridge",
    "root-key",
    "session-export",
    "wip-agent-pay",
    "context-embeddings"
  ]
}
```

## Related

- wipcomputer/wip-ai-devops-toolbox-private#333 ... file-guard workspace fix (separate issue, also discovered Apr 8)
- OpenClaw 2026.4.8 changelog ... tools.allow enforcement change
- `/Users/lesa/.openclaw/extensions/wip-1password/node_modules/openclaw/docs/tools/index.md` ... tool groups and allowlist docs
