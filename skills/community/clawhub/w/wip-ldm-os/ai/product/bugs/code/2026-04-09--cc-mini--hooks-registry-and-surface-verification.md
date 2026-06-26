# Hooks: registry, surface verification, and installer integration

**Date:** 2026-04-09
**Reporter:** cc-mini (with Parker)
**Component:** Claude Code (wip-ai-devops-toolbox), ldm install
**Severity:** high

## Problem

There is no single source of truth for which hooks are installed on which surfaces. Hooks are registered in three different places (git hooks directory, Claude Code settings.json, OpenClaw plugin system) with no unified view. When a hook fails or is missing, there's no way to verify it's installed correctly across all surfaces.

Today's incident: `git lfs install` overwrote the git hooks directory, destroying the pre-commit hook. Nobody knew until hours later. There was no verification, no alert, no registry that tracked the hook's status.

## What exists now

A `hooks/registry.json` was created at `~/.ldm/hooks/registry.json` (2026-04-09) as scaffolding. It lists all 13 hooks with their owner, type, surfaces, source, and deployer. But nothing reads it and nothing keeps it in sync.

## What needs to happen

### 1. Installer reads and writes hooks/registry.json

When `ldm install` deploys a hook (git hook, Claude Code hook, or OpenClaw plugin), it should:
1. Register the hook in `~/.ldm/hooks/registry.json`
2. Record which surfaces it was deployed to
3. Verify the hook is actually active on each surface (file exists, settings.json entry exists, plugin loaded)

### 2. ldm doctor verifies hooks across surfaces

`ldm doctor` should read `hooks/registry.json` and verify:
- Git hooks: file exists at `~/.ldm/hooks/{name}`, is executable, `core.hooksPath` is set
- Claude Code hooks: entry exists in `~/.claude/settings.json` hooks section, command path is valid
- OpenClaw hooks: plugin exists at `~/.openclaw/extensions/{name}/`, gateway logs show it loaded

Report any hook that's registered but not active on its expected surface.

### 3. Installer protects git hooks from git lfs install

`git lfs install` overwrites the hooks directory. The installer must:
- Check if our hooks exist after LFS installation
- Restore any missing hooks from templates
- Or: use a combined hook approach where LFS and our hooks coexist

### 4. Generate hook docs from registry

Same as extension docs: `ldm install` should auto-generate `~/.ldm/library/documentation/hooks/` from `hooks/registry.json`. Each hook doc shows surfaces, verification status, and how to test.

### 5. Hook health in daily audit

The workspace audit (`workspace-audit.sh`) should check:
- All hooks in registry exist on their expected surfaces
- No hooks were overwritten (compare file hash to expected)
- Alert if a hook is missing or modified

## Files to change

- `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/bin/ldm.js` ... hook registration in installer, doctor verification
- `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/lib/deploy.mjs` ... hook deployment with registry update
- `/Users/lesa/wipcomputerinc/repos/ldm-os/devops/wip-ai-devops-toolbox-private/tools/ldm-jobs/workspace-audit.sh` ... hook health check

## Related

- `~/.ldm/hooks/registry.json` (created 2026-04-09, scaffolding)
- `~/.ldm/library/documentation/hooks/` (hook docs)
- `~/.ldm/library/documentation/how-hooks-work.md` (system doc)
- `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/bugs/installer/2026-04-09--cc-mini--installer-must-generate-extension-docs.md` (same pattern for extensions)
- `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/plans-prds/agent-memories/2026-04-09--cc-mini--memory-integrity-and-protection.md` (hooks protect memories)
- `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/bugs/master-plans/2026-04-09--cc-mini--master-plan-004-execution-order.md`
