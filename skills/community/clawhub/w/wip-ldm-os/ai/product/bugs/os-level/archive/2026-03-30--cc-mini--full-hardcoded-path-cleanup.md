# Bug: Full hardcoded path cleanup across all repos

**Date:** 2026-03-30
**Filed by:** cc-mini
**Priority:** high
**Related:** 2026-03-30--cc-mini--hardcoded-paths-audit.md (deployed extension audit)

## Problem

Comprehensive scan of all repos on disk. Every hardcoded path that should be a config variable. Some are the old iCloud path (broken). Some are `/Users/lesa` fallbacks (won't work for other users). All need to read from config.

## Scan results

### CRITICAL: Old iCloud path (broken, path doesn't exist)

| Repo | File | Line | Hardcoded |
|------|------|------|-----------|
| memory-crystal-private | `src/dev-update.ts:11` | STAFF_DIR | `~/Documents/wipcomputer--mac-mini-01/staff` |
| wip-private-mode-private | `src/locations.ts:1001-1002` | dev-updates dirs | `~/Documents/wipcomputer--mac-mini-01/staff/Lēsa/...` and Parker's |
| wip-ai-devops-toolbox-private | `tools/ldm-jobs/backup.sh:5` | SCRIPT path | `~/Documents/wipcomputer--mac-mini-01/staff/Lēsa/scripts/...` |
| wip-ldm-os-private | `bin/scaffold.sh:14` | CC_DOCS | `~/Documents/wipcomputer--mac-mini-01/staff/Parker/...` |
| wip-ldm-os-private | `src/boot/boot-hook.mjs:104` | journals dir | `~/Documents/wipcomputer--mac-mini-01/staff/Parker/...` |
| cc-session-export (_to-privatize) | 3 files | OUTPUT_DIR | `~/Documents/wipcomputer--mac-mini-01/staff/...` |

### NEEDS CONFIG: /Users/lesa fallbacks

These use `process.env.HOME || '/Users/lesa'` which works on this machine but breaks for any other user.

| Repo | File | Line | What |
|------|------|------|------|
| memory-crystal-private | `scripts/migrate-lance-to-sqlite.mjs:26` | openclawHome | `'/Users/lesa'` fallback |
| wip-bridge-private | `src/index.ts:31` | METRICS_DIR | `'/Users/lesa'` fallback |
| wip-private-mode-private | `src/openclaw.ts:9` | CONFIG_DIR | `'/Users/lesa'` fallback |
| wip-private-mode-private | `src/locations.ts:9` | HOME | `'/Users/lesa'` fallback |
| wip-ldm-os-private | `src/bridge/mcp-server.ts:31` | METRICS_DIR | `'/Users/lesa'` fallback |

### NEEDS VAR: Hardcoded in test files

| Repo | File | Line | What |
|------|------|------|------|
| wip-ai-devops-toolbox-private | `tools/wip-branch-guard/test.sh:113` | Plan file path | `/Users/lesa/.claude/plans/my-plan.md` |

### _to-privatize repos (not yet migrated)

| Repo | Files | What |
|------|-------|------|
| imessage-rich | 1 | `/Users/lesa` reference |
| voice-training-plugin | 2 | Archive paths |
| lesa-openclaw-context-embeddings | 1 | `/Users/lesa` reference |
| cc-session-export | 3 | Old iCloud session paths (deprecated but still deployed) |

## Already fixed (deployed, source PRs merged)

These were fixed earlier today (Mar 30):
- memory-crystal-private `src/dev-update.ts` (PR #98, `resolveWorkspace()`)
- wip-private-mode-private `src/locations.ts` (PR #1, `resolveWorkspace()`)
- session-export OpenClaw plugin (PR #1, `resolveWorkspace()`)

## Fix pattern

Every hardcoded path should use one of:
1. `resolveWorkspace()` ... reads `~/.ldm/config.json` workspace key
2. `process.env.HOME` ... for home directory (no `/Users/lesa` fallback, use `os.homedir()`)
3. `process.env.OPENCLAW_DIR || join(HOME, '.openclaw')` ... for OpenClaw paths

## Config vars needed in `~/.ldm/config.json`

| Key | Current value | Used by |
|-----|--------------|---------|
| `workspace` | `/Users/lesa/wipcomputerinc` | All plugins needing team/repo paths |
| `paths.ldm` | `~/.ldm` | LDM internal paths |
| `paths.claude` | `~/.claude` | Claude Code paths |
| `paths.openclaw` | `~/.openclaw` | OpenClaw paths |

These all exist in the config already. The plugins just need to read them instead of hardcoding.

## Repos still needing fixes

| Repo | Priority | What |
|------|----------|------|
| wip-ldm-os-private | High | boot-hook.mjs journals path, scaffold.sh CC_DOCS |
| wip-ai-devops-toolbox-private | Medium | ldm-jobs/backup.sh script path, test.sh hardcoded plan path |
| wip-bridge-private | Low | Deprecated repo, `/Users/lesa` fallback only |
| _to-privatize repos | Low | Not migrated yet, fix when privatizing |
