# Plan: OpenClaw Post-Upgrade Smoke Test

**Date:** 2026-04-08
**Author:** Parker + CC Mini
**Component:** ldm install / ldm doctor / openclaw upgrade process
**Triggered by:** OpenClaw 2026.4.8 upgrade silently broke tools.allow, removing all agent filesystem and exec tools

## Problem

When OpenClaw is upgraded, there is no automated verification that the agent still works. The upgrade on Apr 8, 2026 (2026.4.8) silently broke Lēsa's tool access. She lost Read/Write/Exec for hours before anyone noticed. The tools.allow semantics changed between versions and nothing checked.

This has happened before with other config changes (strict Zod validation stripping keys, plugin loading order changes, auth profile format changes). Every upgrade is a risk.

## Goal

After every OpenClaw upgrade, automatically run a smoke test that verifies all critical agent capabilities. If anything fails, warn before the gateway starts serving.

## Where it lives

The smoke test should be part of `ldm doctor` and/or a new `ldm upgrade` post-step in LDM OS (`src/boot/installer.mjs`).

The upgrade runbook is at `repos/ldm-os/devops/open-claw-upgrade-private/UPGRADE-RUNBOOK.md`. The smoke test automates what that runbook checks manually.

## Smoke test checklist

### 1. Gateway health
- [ ] Gateway process is running (`launchctl list | grep openclaw`)
- [ ] HTTP health endpoint returns `{"ok":true}` (`curl localhost:18789/health`)
- [ ] No crash loop (process hasn't restarted more than once in 30 seconds)

### 2. Plugin loading
- [ ] All plugins in `plugins.entries` with `enabled: true` appear in gateway log as "registered"
- [ ] No "plugin failed to initialize" errors in `gateway.err.log`
- [ ] No "Unknown model" errors in `gateway.err.log`

### 3. Tools available (the Apr 8 bug)
- [ ] `tools.allow` (if present) includes core groups: `group:fs`, `group:runtime`, `group:sessions`, `group:memory`
- [ ] Every enabled plugin in `plugins.entries` is listed in `tools.allow` (if the allowlist exists)
- [ ] If `tools.allow` is missing core groups, auto-add them and warn

### 4. Model configuration
- [ ] `agents.defaults.model.primary` resolves to a known model
- [ ] Model warmup succeeds (no "Unknown model" in stderr)
- [ ] Fallback models (if configured) also resolve
- [ ] At least one auth profile has valid credentials for the primary model's provider

### 5. Memory crystal
- [ ] `crystal_status` returns chunk count > 0
- [ ] `crystal_search` returns results for a simple query
- [ ] No embedding API errors in gateway.err.log (except known large-file skips)

### 6. Agent workspace
- [ ] Workspace path exists (`agents.defaults.workspace`)
- [ ] TOOLS.md, MEMORY.md, IDENTITY.md exist in workspace
- [ ] Agent can write to workspace (test write + delete a temp file)

### 7. Channels
- [ ] iMessage channel connects (if enabled)
- [ ] No "channel failed" errors in gateway log

### 8. Auth profiles
- [ ] No stale auth profiles that return billing/credit errors
- [ ] Primary model's provider has at least one valid auth profile

### 9. Config integrity
- [ ] `openclaw doctor` runs without errors
- [ ] No "Unrecognized key" warnings (strict schema)
- [ ] `git diff ~/.openclaw/openclaw.json` shows no unexpected changes from doctor

## Implementation

### Phase 1: ldm doctor integration (quick win)

Add these checks to `ldm doctor`:
- tools.allow audit (check 3)
- Plugin vs tools.allow mismatch detection (check 3)
- Model warmup validation (check 4)
- Workspace file existence (check 6)

These are all static checks that don't require a running gateway.

### Phase 2: ldm upgrade post-step

Add a `postUpgrade()` function to `src/boot/installer.mjs` that runs after OpenClaw is updated:
1. Restart gateway
2. Wait for health endpoint
3. Run full smoke test (checks 1-9)
4. Report pass/fail
5. If critical failures, offer to rollback

### Phase 3: Automated regression

Run the smoke test as a LaunchAgent (like wip-healthcheck) that fires once after each upgrade:
- Detect version change in `meta.lastTouchedVersion`
- Run smoke test
- Report results to agent via chatCompletions endpoint
- Log to `~/.openclaw/logs/upgrade-smoke-YYYY-MM-DD.log`

## Files involved

- **Smoke test logic:** `src/boot/installer.mjs` (new postUpgrade function)
- **Doctor checks:** `src/boot/installer.mjs` or new `src/boot/doctor.mjs`
- **Upgrade runbook:** `repos/ldm-os/devops/open-claw-upgrade-private/UPGRADE-RUNBOOK.md` (add smoke test reference)
- **Config:** `~/.openclaw/openclaw.json` (tools.allow, plugins.entries, agents.defaults)
- **Logs:** `~/.openclaw/logs/gateway.log`, `~/.openclaw/logs/gateway.err.log`

## Related

- wipcomputer/wip-ldm-os#267 ... installer tools.allow bug (the trigger for this plan)
- wipcomputer/wip-ai-devops-toolbox-private#333 ... file-guard workspace fix
- `repos/ldm-os/devops/open-claw-upgrade-private/UPGRADE-RUNBOOK.md` ... manual upgrade steps
- `repos/ldm-os/devops/open-claw-upgrade-private/KNOWN-LANDMINES.md` ... config gotchas
