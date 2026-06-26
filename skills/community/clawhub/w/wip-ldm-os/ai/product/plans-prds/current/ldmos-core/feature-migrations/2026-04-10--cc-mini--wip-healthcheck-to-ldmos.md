# Plan: Migrate wip-healthcheck into LDM OS

**Date:** 2026-04-10
**Author:** Parker + CC Mini
**Component:** wip-healthcheck (external watchdog) -> LDM OS feature
**Source repo:** github.com/wipcomputer/wip-healthcheck (public, currently standalone)
**Current location:** `repos/ldm-os/utilities/_to-privatize/wip-healthcheck/`

## Context

`wip-healthcheck` is an external watchdog for OpenClaw/LDM OS. It runs as a macOS LaunchAgent every 3 minutes, probes the gateway HTTP endpoint, monitors file descriptors, token usage, and memory-crystal health, and auto-restarts the gateway if probes fail. It's the only external process that catches stuck-state conditions (crash loops, token exhaustion, hanging sessions).

**Current state:** The repo lives at `github.com/wipcomputer/wip-healthcheck` as a standalone public repo. On this machine it's cloned into `repos/ldm-os/utilities/_to-privatize/wip-healthcheck/`. The `_to-privatize/` prefix means it's staged for migration but the migration hasn't happened yet.

**Why this matters:** On Apr 10, 2026 the healthcheck was discovered to be non-functional. The LaunchAgent was pointing at `~/.openclaw/wip-healthcheck/healthcheck.mjs` but the file didn't exist. The old installer pattern (`wip-healthcheck-private/install.sh`) expects a sibling public repo clone at `utilities/wip-healthcheck/`, which doesn't exist on this machine because **we do not clone public repos**. The installer silently no-ops because of an `if [ -d ... ]` check, leaving the healthcheck broken without any error.

The same day, we also discovered the probe endpoint was hitting `/` (which returns 503 when Control UI assets are missing) instead of `/health`. The broken probe caused unnecessary gateway restarts every 3 minutes on every OpenClaw install where `pnpm ui:build` hadn't run. That fix shipped as wipcomputer/wip-healthcheck#5 and was manually deployed.

This plan migrates the healthcheck from a standalone tool into a proper LDM OS feature following the same pattern as other rolled-in tools (wip-release, wip-file-guard, wip-branch-guard).

## Goal

Make `ldm install` deploy a working healthcheck, end-to-end:
1. Install the script to a stable runtime path
2. Install the LaunchAgent plist pointing at that path
3. Resolve config from `~/.ldm/config.json` or equivalent
4. Ensure probe, escalation, and logs all work on fresh machines
5. Leave no orphaned clones in `_to-privatize/`

## Current architecture (before migration)

```
Source repo (public):   github.com/wipcomputer/wip-healthcheck
                         |
                         v
Clone location:          repos/ldm-os/utilities/_to-privatize/wip-healthcheck/
  - healthcheck.mjs      (main script, ~21KB)
  - config.example.json
  - install.sh           (deploys plist + uses $SCRIPT_DIR/healthcheck.mjs)
  - backup.sh            (separate concern, backup system)
  - install-backup.sh
                         |
                         v
Private config repo:    repos/ldm-os/utilities/wip-healthcheck-private/
  - config.json          (actual production config with tokens, contact)
  - install.sh           (copies config.json + calls public install.sh)
                         |
                         v
Runtime (deployed):      ~/.openclaw/wip-healthcheck/
  - config.json          (deployed by private installer)
  - healthcheck.mjs      (manually deployed Apr 10, should be by installer)
  - state.json           (created by script at first run)
  - logs/                (created by script)

LaunchAgent:             ~/Library/LaunchAgents/ai.openclaw.healthcheck.plist
  - Runs every 180s
  - stdout -> ~/.ldm/logs/healthcheck-stdout.log
  - stderr -> ~/.ldm/logs/healthcheck-stderr.log
```

## Target architecture (after migration)

Same pattern as wip-file-guard and wip-branch-guard: source lives in LDM OS, installer deploys, public mirror handles external contributions.

```
Source (private):       repos/ldm-os/wip-ldm-os-private/src/healthcheck/
                         - core.mjs              (the probe + remediation logic)
                         - launchd/plist.mjs     (generates the plist)
                         - install.mjs           (installs to runtime location)
                         - README.md             (for AI agents, per LDM OS convention)

Source (public mirror): repos/ldm-os/wip-ldm-os-private/ + deploy-public.sh
                         Synced to github.com/wipcomputer/wip-ldm-os

Installer integration:  repos/ldm-os/wip-ldm-os-private/src/boot/installer.mjs
                         - Calls src/healthcheck/install.mjs on `ldm install`
                         - Reads healthcheck config from ~/.ldm/config.json

Runtime (deployed):     ~/.ldm/extensions/wip-healthcheck/
                         - healthcheck.mjs      (copied by ldm install)
                         - config.json          (merged from ~/.ldm/config.json healthcheck section)
                         - state.json           (created by script)

LaunchAgent:             ~/Library/LaunchAgents/ai.openclaw.healthcheck.plist
                         - Generated by installer, pointing at ~/.ldm/extensions/wip-healthcheck/healthcheck.mjs
                         - stdout/stderr unchanged
```

## Migration phases

### Phase 1: Create private+public split (no code changes yet)

Before rolling into LDM OS, the standalone repo needs a private/public split per WIP convention (public/private repo rule from CLAUDE.md).

1. Create `github.com/wipcomputer/wip-healthcheck-private`
2. Move current `wip-healthcheck` contents into private repo
3. Add `ai/` directory with plans, todos, dev updates
4. Set up `deploy-public.sh` to sync non-ai content to public `wip-healthcheck`
5. Archive the existing public repo history in private (preserve attribution)

**Files involved:**
- New repo: `wip-healthcheck-private`
- Existing public: `wip-healthcheck` (becomes mirror)

**Verification:** Private repo has full history + ai/. Public repo has everything except ai/.

### Phase 2: Move source into LDM OS

Once the private/public split is done, fold the source into LDM OS the same way wip-file-guard and wip-branch-guard are folded.

1. Create `src/healthcheck/` in wip-ldm-os-private
2. Port `healthcheck.mjs` to `src/healthcheck/core.mjs` (adjust __dirname logic for new location)
3. Port `install.sh` to `src/healthcheck/install.mjs` (generates plist, copies script)
4. Add `src/healthcheck/README.md` per LDM OS agent-readable convention
5. Merge `wip-healthcheck-private`'s config.example into LDM OS config schema (`~/.ldm/config.json` gets a `healthcheck` section)
6. Archive `wip-healthcheck-private` repo (read-only reference)
7. Archive standalone `wip-healthcheck` repo (deprecate with README pointing at LDM OS)

**Files involved:**
- `repos/ldm-os/wip-ldm-os-private/src/healthcheck/core.mjs` (new)
- `repos/ldm-os/wip-ldm-os-private/src/healthcheck/install.mjs` (new)
- `repos/ldm-os/wip-ldm-os-private/src/healthcheck/README.md` (new)
- `repos/ldm-os/wip-ldm-os-private/src/boot/installer.mjs` (update to call healthcheck install)
- `~/.ldm/config.json` schema extension

**Verification:** Source builds and runs from `src/healthcheck/core.mjs`. Tests pass. README explains the component.

### Phase 3: Integrate with `ldm install`

Make `ldm install` deploy the healthcheck automatically.

1. Update `src/boot/installer.mjs` to call `src/healthcheck/install.mjs` during install
2. `install.mjs` should:
   - Read healthcheck config from `~/.ldm/config.json`
   - Copy `core.mjs` to `~/.ldm/extensions/wip-healthcheck/healthcheck.mjs`
   - Write merged config to `~/.ldm/extensions/wip-healthcheck/config.json`
   - Generate plist at `~/Library/LaunchAgents/ai.openclaw.healthcheck.plist` pointing at the new path
   - Unload + bootstrap the LaunchAgent
3. `ldm doctor` should verify:
   - Script exists at expected path
   - Config is present
   - LaunchAgent is loaded and running
   - Last exit code was 0
   - Recent log output is clean

**Files involved:**
- `src/boot/installer.mjs` (call healthcheck install)
- `src/boot/doctor.mjs` (add healthcheck verification)
- `~/.ldm/extensions/wip-healthcheck/` (new runtime location)

**Verification:** `ldm install` on a fresh machine deploys a working healthcheck. `ldm doctor` reports it healthy.

### Phase 4: Migrate runtime path

The current runtime path is `~/.openclaw/wip-healthcheck/` but everything else is under `~/.ldm/extensions/`. Consolidate.

1. Installer deploys to `~/.ldm/extensions/wip-healthcheck/` (new canonical path)
2. Installer uninstalls the old `~/.openclaw/wip-healthcheck/` LaunchAgent
3. Installer removes the old `~/.openclaw/wip-healthcheck/` directory
4. Add compatibility: if old path still has a running LaunchAgent, gracefully migrate

**Files involved:**
- `src/healthcheck/install.mjs` (add uninstall of old path)
- `src/boot/installer.mjs` (one-time migration step)

**Verification:** After `ldm install`, no files remain at `~/.openclaw/wip-healthcheck/`. New LaunchAgent points at `~/.ldm/extensions/wip-healthcheck/healthcheck.mjs`.

### Phase 5: Cleanup

1. Delete `repos/ldm-os/utilities/_to-privatize/wip-healthcheck/` (migration complete)
2. Delete `repos/ldm-os/utilities/wip-healthcheck-private/` (folded into LDM OS)
3. Archive `github.com/wipcomputer/wip-healthcheck-private` (read-only reference)
4. Update `github.com/wipcomputer/wip-healthcheck` README to point at LDM OS
5. Update CLAUDE.md references from old install path to new

**Files involved:**
- `_to-privatize/wip-healthcheck/` (delete)
- `utilities/wip-healthcheck-private/` (delete)
- CLAUDE.md references (update)

**Verification:** `grep -r wip-healthcheck` shows only LDM OS references. `grep -r "_to-privatize/wip-healthcheck"` returns nothing. Clean repo tree.

## Dependency order

```
Phase 1 (privatize standalone repo)
  |
  +-- Phase 2 (move source into LDM OS)
       |
       +-- Phase 3 (integrate with ldm install)
            |
            +-- Phase 4 (migrate runtime path)
                 |
                 +-- Phase 5 (cleanup)
```

Phases 2 and 3 can be combined into one PR since they're tightly coupled. Phase 4 should be separate so runtime migration is atomic and reversible. Phase 5 is pure cleanup after everything else is stable.

## Known issues to fix during migration

These are already-identified bugs. The migration is a natural place to fix them.

1. **Probe endpoint** (fixed Apr 10 in wipcomputer/wip-healthcheck#5) ... merge into LDM OS port.
2. **Escalation path broken** ... agent chatCompletions returns ECONNRESET. Need to fix the chat endpoint call, or make escalation via bridge inbox instead.
3. **Crystal errors false positive** ... the watchdog flags 3 "crystal errors" that are actually the known large-file embedding skips (MEMORY-v1-backup, TODO-from-history, lesa-full-history). Filter these from the error count.
4. **No iMessage fallback contact** ... `config.escalation.escalationContact` is empty. Either require it during `ldm init`, or remove the iMessage path in favor of bridge-based escalation.
5. **Silent install failure** ... the `wip-healthcheck-private/install.sh` bails quietly if the public repo isn't cloned. Migration removes this entire code path.

## Files involved summary

| Phase | File | What |
|------|------|------|
| 1 | New repo: wip-healthcheck-private | Create with full history |
| 1 | New: deploy-public.sh | Sync script |
| 2 | wip-ldm-os-private/src/healthcheck/core.mjs | Ported healthcheck script |
| 2 | wip-ldm-os-private/src/healthcheck/install.mjs | Installer logic |
| 2 | wip-ldm-os-private/src/healthcheck/README.md | Agent docs |
| 3 | wip-ldm-os-private/src/boot/installer.mjs | Call healthcheck install |
| 3 | wip-ldm-os-private/src/boot/doctor.mjs | Add healthcheck checks |
| 3 | ~/.ldm/config.json schema | Add healthcheck section |
| 4 | wip-ldm-os-private/src/healthcheck/install.mjs | Add old-path migration |
| 5 | _to-privatize/wip-healthcheck/ | Delete |
| 5 | utilities/wip-healthcheck-private/ | Delete |
| 5 | CLAUDE.md references | Update |

## Related

- `ai/product/bugs/installer/2026-04-08--cc-mini--tools-allow-not-updated-on-plugin-install.md` ... same migration shape
- `ai/product/plans-prds/current/openclaw-upgrade/2026-04-08--cc-mini--post-upgrade-smoke-test.md` ... post-upgrade smoke test should verify healthcheck is running
- `ai/product/bugs/master-plans/2026-04-08--cc-mini--master-plan-003-pipeline-consolidation.md` ... consolidation master plan this feeds into
- `github.com/wipcomputer/wip-healthcheck` ... current public repo
- `repos/ldm-os/utilities/_to-privatize/` ... staging area for other pending migrations (imessage-reply-context, imessage-rich, lesa-voice-call, md-to-x, openclaw-tavily, security-audit-skill, wip-obsidian, wip-understand-video)

## Other `_to-privatize/` candidates

The `_to-privatize/` folder has 9 tools waiting for similar migration. This plan is the template for the rest:
- imessage-reply-context
- imessage-rich
- lesa-voice-call
- md-to-x
- openclaw-tavily
- security-audit-skill
- wip-healthcheck (this plan)
- wip-obsidian
- wip-understand-video

Each follows the same 5-phase pattern: privatize -> move into LDM OS -> integrate installer -> migrate runtime path -> cleanup.
