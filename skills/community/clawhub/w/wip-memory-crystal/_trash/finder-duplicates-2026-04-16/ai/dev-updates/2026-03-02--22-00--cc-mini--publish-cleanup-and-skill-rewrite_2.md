# Dev Update: Publish Cleanup, SKILL.md Rewrite, Process Fixes

**Date:** 2026-03-02 22:00 PST
**Author:** CC-Mini
**Versions:** v0.3.1 through v0.3.3

---

## What Happened

### npm Leak Recovery (completed)

All three leaked npm packages (memory-crystal 0.2.0, 0.3.0, markdown-viewer 1.2.5) were unpublished. Clean versions published:
- `memory-crystal@0.3.1` ... clean, 74 files, 135KB (down from 503KB with ai/ leak)
- `@wipcomputer/markdown-viewer@1.2.6` ... clean, 78 files
- `.npmignore` deployed across 6 repos

### SKILL.md Rewrite (v0.3.2)

SKILL.md is now a complete agent install guide. When a user pastes the README prompt into their AI, the agent reads SKILL.md and does everything:

1. `npm install -g memory-crystal`
2. Detects all runtimes (Claude Code CLI, Claude Desktop, OpenClaw)
3. Installs MCP server for each detected runtime
4. Sets up embeddings (OpenAI, Ollama, or Google)
5. Runs `crystal init`
6. Verifies with `crystal_status`

The user says "yes" and the agent handles the rest. This is the onboarding experience.

### crystal-mcp Binary (v0.3.2, fixed v0.3.3)

Added `crystal-mcp` as a package.json bin entry. MCP server config is now just:
```bash
claude mcp add --scope user memory-crystal -- crystal-mcp
```

v0.3.2 had a bug: npm stripped the bin entries because paths used `./dist/` prefix. Fixed in v0.3.3 by removing the prefix. Both `crystal` and `crystal-mcp` commands verified working from global npm install.

### CLI Search Output (v0.3.2)

CLI `crystal search` now matches the MCP server output: numbered results, freshness icons, same format. End users get the same experience regardless of interface.

### Public Repo Sync

- Public memory-crystal repo synced (v0.3.1, v0.3.3)
- Removed accidentally synced `.wrangler/` local dev state from public repo
- Public markdown-viewer repo synced (v1.2.6)
- deploy-public.sh fixed: `--squash` changed to `--merge`, added rsync exclusions for `.wrangler/`, `.claude/`, `CLAUDE.md`

### wip-release Improved

`buildReleaseNotes()` now categorizes commits into Changes/Fixes/Docs sections, excludes `ai/` from diffstats, adds Built-by attribution. v0.3.1 release notes rewritten to be exhaustive (OpenClaw-level quality).

### Org README Fixed

OpenClaw link changed from `wipcomputer/openclaw` (fork) to `openclaw/openclaw` (upstream).

### No-Squash Rule Enforced

- deploy-public.sh uses `--merge` instead of `--squash`
- Dev Guide private has "Release Notes Standard" section

## Current State

- `memory-crystal@0.3.3` live on npm, clean, bin entries working
- `@wipcomputer/markdown-viewer@1.2.6` live on npm, clean
- Public repos synced
- SKILL.md is a complete agent install guide
- wip-release generates structured release notes
- All process fixes documented in Dev Guide

## What's Next

### Parker's Testing
- [ ] Local Memory: verified working (169K chunks)
- [ ] Agent install flow: paste README prompt into fresh Claude Code session
- [ ] Multi-Device Sync: blocked by SA token AirDrop to Air
- [ ] Cloud Memory: blocked by R2 enable + Worker deploy

### CC-Mini's Next
- [ ] Phase 2: Health monitoring (`crystal health` CLI, wip-healthcheck integration)
- [ ] Cloud deploy (after Parker enables R2)
- [ ] Dream Weaver integration (point DW at transcripts, automate schedule)

## Files Changed

| File | Change |
|------|--------|
| `package.json` | Added crystal-mcp bin, version 0.3.3, fixed ./ prefix |
| `skills/memory/SKILL.md` | Complete rewrite as agent install guide |
| `src/cli.ts` | Search output matches MCP (freshness icons, numbered) |
| `CHANGELOG.md` | v0.3.1, v0.3.2, v0.3.3 entries |
| `wip-dev-tools-private/tools/wip-release/core.mjs` | Categorized release notes |
| `wip-dev-tools-private/guide/scripts/deploy-public.sh` | --merge, rsync exclusions |
| `wip-dev-tools-private/ai/DEV-GUIDE-private.md` | Release notes standard, .npmignore |
