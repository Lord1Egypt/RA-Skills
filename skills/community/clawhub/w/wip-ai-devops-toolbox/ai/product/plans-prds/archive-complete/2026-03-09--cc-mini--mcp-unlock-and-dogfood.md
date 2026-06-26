# Plan: MCP Unlock + Dogfood the Installer

**Date:** 2026-03-09
**Author:** cc-mini
**Version target:** v1.4.0

## Problem

We built the Universal Installer to give every tool six interfaces (CLI, Module, MCP Server, OpenClaw Plugin, Skill, Claude Code Hook). But we never ran it on our own tools. Zero MCP servers across all 9 tools. The agents can't call wip-release, wip-license-hook, or wip-repos natively. We're not eating our own cooking.

## Architecture: How it should work

```
repo (source)
  -> wip-install (detect + deploy)
    -> ~/.ldm/extensions/<name>/     (installed runtime)
      -> ~/.openclaw/extensions/     (symlink, Lesa sees it)
      -> ~/.claude/settings.json     (CC Hook registered)
      -> .mcp.json                   (MCP server registered)
```

This is the same path plugins already use. The installer just automates it.

## Interface coverage gap (current state)

| Tool | CLI | Module | MCP | OpenClaw | Skill | CC Hook |
|------|-----|--------|-----|----------|-------|---------|
| wip-universal-installer | Y | - | - | - | Y | - |
| wip-release | Y | Y | - | - | Y | - |
| wip-license-hook | Y | - | - | - | Y | - |
| wip-repo-permissions-hook | Y | Y | - | Y | Y | Y |
| post-merge-rename | Y | - | - | - | - | - |
| wip-file-guard | Y | - | - | Y | Y | Y |
| deploy-public | Y | - | - | - | - | - |
| wip-repos | Y | Y | - | - | - | - |
| ldm-jobs | - | - | - | - | - | - |

## Steps

### Phase 1: Missing SKILL.md files (3 tools)

1. Write `tools/wip-repos/SKILL.md`
2. Write `tools/deploy-public/SKILL.md` (may need to create a wrapper folder with package.json around the shell script)
3. Write `tools/post-merge-rename/SKILL.md` (same)

### Phase 2: MCP servers (4 core tools)

Each gets a `mcp-server.mjs` that wraps the tool's core logic as MCP tools.

4. `tools/wip-release/mcp-server.mjs`
   - Tools: `release(level, notes, dryRun)`, `release_status()`
   - Wraps `core.mjs`

5. `tools/wip-license-hook/mcp-server.mjs`
   - Tools: `license_scan(path)`, `license_audit(path)`
   - Wraps the compiled `dist/` output

6. `tools/wip-repo-permissions-hook/mcp-server.mjs`
   - Tools: `repo_permissions_check(repo)`, `repo_permissions_audit(org)`
   - Wraps `core.mjs`

7. `tools/wip-repos/mcp-server.mjs`
   - Tools: `repos_check()`, `repos_sync(dryRun)`, `repos_add(path, remote)`, `repos_move(from, to)`, `repos_tree()`
   - Wraps `core.mjs`

### Phase 3: Dev Guide rules (both guides)

8. Add "Universal Installer Checklist" section to DEV-GUIDE-GENERAL-PUBLIC.md:
   - Run `wip-install --dry-run` before every release
   - Minimum for agent-callable: Module + Skill + MCP Server
   - Sub-tool checklist for toolbox repos

9. Add matching section to ai/DEV-GUIDE-FOR-WIP-ONLY-PRIVATE.md:
   - Same rules plus: deploy to ~/.ldm/extensions/, symlink to OpenClaw
   - After wip-release, run wip-install on the toolbox itself

### Phase 4: Dogfood

10. Run `wip-install` on each tool in the toolbox
11. Verify all interfaces detected
12. Deploy to ~/.ldm/extensions/wip-dev-tools/
13. Symlink to ~/.openclaw/extensions/
14. Register MCP server in .mcp.json
15. Test: have Lesa call wip-release via MCP

### Phase 5: Release

16. PR to wip-dev-tools-private main
17. `wip-release minor --notes="MCP unlock: all core tools now agent-callable"`
18. `deploy-public.sh`
19. Update org profile if needed

## Not in scope

- ldm-jobs: shell scripts for cron, doesn't need MCP. Maybe a Skill later.
- OpenClaw plugins for tools that don't need lifecycle hooks (wip-release, wip-repos). MCP is enough.
- CC Hooks for tools that don't guard anything (wip-release, wip-repos). MCP is enough.

## Success criteria

Every tool that has core logic is callable by Lesa via MCP without shelling out. The installer proves it works by installing the toolbox itself.
