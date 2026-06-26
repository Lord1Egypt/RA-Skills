# Release Notes: wip-ldm-os v0.4.67

**Date:** 2026-03-30

## What changed

### Hardcoded path removal

Three files had `/Users/lesa` hardcoded. All now use portable alternatives.

**boot-hook.mjs** had the journals directory path hardcoded to `/Users/lesa/wipcomputerinc/team/cc-mini/documents/journals/`. The boot hook now reads the LDM agents path from config to locate journal files, so it works on any machine regardless of username or workspace location (#266).

**scaffold.sh** had `CC_DOCS` hardcoded to a path under `/Users/lesa/wipcomputerinc/`. It now reads the workspace root from LDM config via the unified settings file, making scaffolding portable across machines (#266).

**bridge/mcp-server.ts** used `/Users/lesa` as a fallback when resolving the OpenClaw home directory. It now calls `os.homedir()` to build the path dynamically (#266).

### Hardcoded path audit

A full audit was performed across all LDM OS repos and plugins to identify every instance of hardcoded `/Users/lesa` paths. The audit document catalogs findings across memory-crystal, private-mode, devops-toolbox, healthcheck, and other components. Each repo received targeted fixes in its own PR (#265).

### Bridge file-based messaging (Phases 1-4)

The bridge moved from in-memory inbox to file-based messaging. Bridge now deploys to both harness locations, supports scope headers for routing, has session routing, and the installer deploys bridge on CLI update. OpenClaw version is pinned, cc-watcher is disabled, config is merged, and backup config reads from unified config (#267).

### Planning docs

Added bridge messaging architecture plan, iOS app as Core plan, iCloud relay + iOS MCP server feasibility research, bridge plan alignment with master plan, skills spec cross-reference, Phase 5 Cloud Relay plan (Cloudflare + CloudKit), and several bug reports for session export paths and hardcoded path issues (#258, #259, #260, #261, #262, #263, #264, #268).

## Why

The hardcoded paths broke on any machine where the username is not `lesa`. The boot hook, scaffold, and bridge are all critical paths. If boot-hook can't find journals, CC loses its warm-start narrative. If scaffold creates files at wrong paths, worktree setup breaks. If the bridge can't resolve homedir, agent-to-agent communication fails. Part of a broader audit across all LDM OS repos to eliminate hardcoded user paths and make everything portable.

## Issues closed

- Closes #253
- #258, #259, #260, #261, #262, #263, #264, #265, #266, #267, #268

## How to verify

```bash
grep -r "/Users/lesa" src/ scripts/ bridge/ --include="*.ts" --include="*.mjs" --include="*.sh"
# Should return zero results (excluding ai/ docs and test fixtures)
```
