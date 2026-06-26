# Plan: LDM OS Boot Sequence Hook

## Context

CC (Claude Code CLI) has a 10-step boot sequence defined in CLAUDE.md that must run every session. Currently it depends on the agent choosing to read the files. The agent frequently forgets, causing cascading failures: doesn't know repo locations, guesses paths, touches wrong folders. This happened again on 2026-03-11.

The fix: a `SessionStart` hook that mechanically reads boot files and injects them into context via `additionalContext` before the agent ever sees the first user message. No relying on the agent to remember.

This is the Boot Sequence pillar of LDM OS (one of four: Memory Crystal, Dream Weaver, Sovereignty Covenant, Boot Sequence).

## Repo and Deploy Locations

- **Source:** `wip-ldm-os-private/src/boot/` (branch: `cc-mini/boot-hook`)
- **Deploy:** `~/.ldm/shared/boot/` (matches the architecture in wip-ldm-os-private README line 56)
- **Hook registration:** `~/.claude/settings.json` (add SessionStart entry)

## Files to Create

### 1. `src/boot/boot-hook.mjs` (the hook script)

Node.js ES module. Zero dependencies (only `node:fs`, `node:path`). Follows the exact pattern from `guard.mjs`:

```
1. Read stdin JSON
2. Load boot-config.json from import.meta.dirname
3. For each boot step:
   - Read the file (or most recent file in a directory)
   - Truncate if over the configured line limit
   - Skip gracefully if missing, log to stderr
4. Assemble into structured additionalContext string
5. Output JSON: { hookSpecificOutput: { hookEventName: "SessionStart", additionalContext: "..." } }
6. Exit 0 always (never block session startup)
```

**What gets loaded (content budget ~700 lines, ~3,500 tokens, under 2% of context):**

| Step | File | Strategy | Lines |
|------|------|----------|-------|
| 1 | CLAUDE.md | SKIP (already loaded by Claude Code) | 0 |
| 2 | SHARED-CONTEXT.md | Full | ~64 |
| 3 | Most recent journal (Parker's) | First 80 lines | ~80 |
| 4 | Workspace daily logs (today + yesterday) | Last 40 lines each | ~80 |
| 5 | cc-full-history.md | Reminder line only (too large) | 2 |
| 6 | CC CONTEXT.md | Full | ~53 |
| 7 | CC SOUL.md | Full | ~150 |
| 8 | Most recent CC journal | First 80 lines | ~80 |
| 9 | CC daily log (today, fallback yesterday) | Last 60 lines | ~60 |
| 10 | repo-locations.md | Full | ~104 |

**Assembly format:**
```
== LDM OS BOOT SEQUENCE (loaded automatically by SessionStart hook) ==

== [Step 2] SHARED-CONTEXT.md ==
<content>

== [Step 6] CC CONTEXT.md ==
<content>

...

== Boot complete. Loaded N/9 files. Skipped: <list>. ==
```

### 2. `src/boot/boot-config.json` (paths and limits)

```json
{
  "agentId": "cc-mini",
  "timezone": "America/Los_Angeles",
  "steps": {
    "sharedContext": {
      "path": "~/.openclaw/workspace/SHARED-CONTEXT.md",
      "critical": true
    },
    "journals": {
      "dir": "~/Documents/wipcomputer--mac-mini-01/staff/Parker/Claude Code - Mini/documents/journals",
      "maxLines": 80,
      "strategy": "most-recent"
    },
    "workspaceDailyLogs": {
      "dir": "~/.openclaw/workspace/memory",
      "maxLines": 40,
      "days": ["today", "yesterday"]
    },
    "fullHistory": {
      "reminder": "Read on cold start: staff/Parker/Claude Code - Mini/documents/cc-full-history.md"
    },
    "context": {
      "path": "~/.ldm/agents/cc-mini/CONTEXT.md",
      "critical": true
    },
    "soul": {
      "path": "~/.ldm/agents/cc-mini/SOUL.md"
    },
    "ccJournals": {
      "dir": "~/.ldm/agents/cc-mini/memory/journals",
      "maxLines": 80,
      "strategy": "most-recent"
    },
    "ccDailyLog": {
      "dir": "~/.ldm/agents/cc-mini/memory/daily",
      "maxLines": 60,
      "days": ["today", "yesterday"]
    },
    "repoLocations": {
      "path": "~/.claude/projects/-Users-lesa--openclaw/memory/repo-locations.md",
      "critical": true
    }
  }
}
```

Config uses `~` shorthand resolved to `os.homedir()` at runtime. Portable across machines. Future agents (cc-air) just need a different config.

### 3. `src/boot/README.md` (documentation)

Brief docs: what the hook does, how to deploy, how to test, how to add a new boot step.

## Settings.json Change

Add `SessionStart` to the existing `hooks` object in `~/.claude/settings.json`:

```json
"SessionStart": [
  {
    "matcher": "*",
    "hooks": [
      {
        "type": "command",
        "command": "node /Users/lesa/.ldm/shared/boot/boot-hook.mjs",
        "timeout": 15
      }
    ]
  }
]
```

Timeout: 15 seconds. All reads are local filesystem. Should complete under 2 seconds. 15s gives margin for iCloud latency.

## Error Handling

**Principle: partial boot is better than no boot. No boot is better than a blocked session.**

- stdin parse failure: `process.exit(0)` silently
- Missing file: skip, add to "skipped" list, log to stderr
- Missing directory: same as missing file
- Read error: catch, skip, log
- Config missing: fall back to hardcoded cc-mini paths
- Output too large: hard cap at 2,000 lines, truncate from bottom
- Timeout: Claude Code kills the hook, session starts without boot content

## Deploy Process

```bash
# 1. Create deploy target
mkdir -p ~/.ldm/shared/boot

# 2. Copy from repo
cp src/boot/boot-hook.mjs ~/.ldm/shared/boot/
cp src/boot/boot-config.json ~/.ldm/shared/boot/

# 3. Test manually
echo '{"session_id":"test","hook_event_name":"SessionStart"}' | node ~/.ldm/shared/boot/boot-hook.mjs

# 4. Register in settings.json (edit to add SessionStart hook)

# 5. Restart Claude Code to pick up the new hook
```

No npm install. No build step. Pure ESM, zero dependencies.

## Verification

After deployment, start a new Claude Code session and check:
- [ ] Session starts without errors
- [ ] Agent knows current state from SHARED-CONTEXT.md without being asked
- [ ] Agent knows repo locations without searching
- [ ] Agent references its own identity
- [ ] stderr shows `[boot-hook] loaded N/9 files in Xms`
- [ ] Missing files (steps 3, 5) reported as skipped, not errors

## Implementation Sequence

1. Create branch `cc-mini/boot-hook` on wip-ldm-os-private
2. Create `src/boot/` directory
3. Write `boot-config.json`
4. Write `boot-hook.mjs` (following guard.mjs pattern)
5. Write `README.md`
6. Test locally with piped stdin
7. Deploy to `~/.ldm/shared/boot/`
8. Edit `~/.claude/settings.json` to register the hook
9. Start new session, verify boot content appears
10. Commit, PR, merge
