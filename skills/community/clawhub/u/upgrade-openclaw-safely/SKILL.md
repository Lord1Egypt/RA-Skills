---
name: openclaw-verified-upgrade
description: Use when upgrading OpenClaw, running an OpenClaw upgrade, changing OpenClaw versions, selecting latest vs stable OpenClaw releases, or recovering from partial OpenClaw upgrades where gateway, config, plugins, channels, agents, or runtime availability must remain reliable.
---

# OpenClaw Verified Upgrade

## Overview

Upgrade OpenClaw as a verified state transition, not as a command. The job is complete only when the selected version is installed, the running gateway uses it, **externally-installed plugins (especially `@openclaw/*` official plugins) are compatible with that version**, and the user's critical OpenClaw paths still work.

Convergence is multi-axis: the **host axis** (CLI, service, running process, gateway runtime) and the **plugin axis** (`~/.openclaw/npm` plugins) drift independently. A host that reports the target version is not proof that plugins agree with it.

Default UX: **ordinary-user wizard, expert-grade guardrails**. Keep prompts simple; do the operational analysis internally.

## Non-Negotiable Rules

1. **Latest is not automatically best.** If the user is vague, recommend a stable target, not blind latest.
2. **No command discovery, no command execution.** OpenClaw commands and flags are version-sensitive.
3. **Command exists ≠ command means what you remember.** Confirm semantics from current help/docs/output before critical use.
4. **No release review, no upgrade.** Map target-version changes to the current environment.
5. **No verified backup, no mutation.** Backup must be readable and have a manifest/hash.
6. **One approval does not authorize everything.** Upgrade, restart, config repair, rollback, cache cleanup, daemon edits, and reinstall are separate risk levels.
7. **CLI version ≠ running gateway version.** Verify both.
8. **Gateway alive ≠ user workflow available.** Verify configured critical paths.
9. **Host version ≠ plugin version.** Externally-installed plugins, especially `@openclaw/*`, drift independently of the pinned host. A plugin **newer** than the host can import host SDK entry points that do not exist yet and hard-crash at load time; converge plugins **down** to the host, not the host up to a drifted plugin.
10. **No blind retry.** Classify failure, refresh state, then retry only capped recoverable steps.
11. **No completion claim without evidence.** Report exact checks and outcomes.

## Dangerous Actions Blacklist

These actions are never covered by generic upgrade approval. Ask for explicit authorization and preserve evidence first:

- Deleting OpenClaw state, sessions, caches, plugins, skills, or config directories.
- Running `rm -rf`, destructive cleanup, reinstall, downgrade, or force overwrite as a recovery shortcut.
- Overwriting or restoring config without showing what will change and why.
- Editing LaunchAgent, systemd, daemon, shell profile, or package-manager state.
- Using `sudo` or changing file ownership/permissions.
- Stopping the gateway with stop+start when restart/reload is supported and sufficient.
- Rolling back version or config after state/data migration risk is detected.
- Publishing logs, configs, tokens, session data, or backup contents outside the local machine.

## Wizard Entry

Ask only what is needed:

```text
How should I choose the OpenClaw target version?
1. Recommended stable version (default)
2. Latest version
3. Specific version: ______

If the gateway becomes unhealthy, may I auto-rollback to the pre-upgrade version?
1. Ask me first (default)
2. Auto-rollback if the pre-approved rollback checks pass
```

If the user already specified these, do not ask again.

## State Machine

```text
INTAKE
  -> DISCOVER_ENVIRONMENT
  -> SELECT_TARGET_VERSION
  -> RELEASE_RISK_REVIEW
  -> BUILD_CRITICAL_PATH_CHECKLIST
  -> PREFLIGHT_HEALTH
  -> VERIFIED_BACKUP
  -> USER_CONFIRMATION
  -> EXECUTE_UPGRADE
  -> RESTART_OR_RELOAD
  -> POST_UPGRADE_VERIFICATION
  -> FINAL_REPORT

Any failure -> CLASSIFY_FAILURE -> RETRY_LIMITED | REPAIR_FORWARD | ROLLBACK_IF_AUTHORIZED | STOP_WITH_EVIDENCE
```

Never skip ahead. Each phase must produce evidence or a named blocker.

## Phase Requirements

### 1. Discover Environment

Collect facts before changing anything:

- Current OpenClaw CLI version and path.
- Package/install source: npm, pnpm, brew, source checkout, bundled binary, unknown.
- Running gateway manager: LaunchAgent, systemd, manual process, OpenClaw-managed, unknown.
- Service command/path from service manager, e.g. LaunchAgent plist or process command line.
- Running process command line and binary path when available.
- Config path used by CLI and service.
- Node/npm/brew versions only if relevant to the detected install method.
- Enabled plugins/channels and key agents/bindings. For each plugin record: id, enabled state, install source, **installed version**, install spec, whether it is **pinned**, whether it is an `@openclaw/*` official external plugin, and whether it sits on a critical path. Host-bound official plugins (e.g. Codex) are the ones most likely to break on version skew.
- Active sessions/background jobs if restart may interrupt work.
- Existing health: gateway status, config validity, channel/agent state.

**Path mismatch gate:** compare shell CLI path, package location, service command path, and running process path. If they disagree, identify which one will be upgraded before proceeding.

### 2. Discover Commands and Semantics

Inspect the current installation's command surface. Do not assume historical commands or flags:

- Main help/version command.
- Status/health/doctor commands.
- Gateway lifecycle commands.
- Config validation/apply commands.
- Update/self-update commands.
- Logs command/location.

For critical commands, record what success means. Example: a restart command may only schedule a restart; it is not proof that the new gateway is running.

### 3. Select Target Version

Rules:

- If the user names an exact version, preserve it after availability and compatibility checks.
- If the user asks for latest, verify latest and known risks before recommending it.
- If the user asks for stable/safe/reliable, recommend a conservative stable version with evidence.
- If the user gives a range like `2026.5.x`, choose an exact patch version and explain why.
- If evidence is insufficient, say so; unknown risk is not low risk.

Evidence sources may include npm dist-tags/versions, GitHub releases, OpenClaw changelog/release notes, docs migration notes, local successful upgrade history, and relevant issue reports.

### 4. Release Risk Review

Before upgrade, summarize target-version changes and map them to this environment:

- Breaking changes or migration notes.
- CLI command/lifecycle changes.
- Gateway/daemon/LaunchAgent/systemd changes.
- Config schema/default behavior changes.
- Plugin/channel changes, especially currently enabled ones.
- **Plugin–host version skew.** Compare the target host version against each installed `@openclaw/*` plugin version. Pinning the host without pinning official plugins is a known drift risk: a plugin can auto-update ahead of the host.
- Model/provider/auth/token changes.
- Node/runtime/package-manager requirements.
- State/data migrations and rollback implications.
- Known issues involving gateway, config, channels, plugins, auth, doctor/update, crash/startup.

Risk levels:

- **LOW:** no relevant runtime/config/plugin impact.
- **MEDIUM:** command/config/plugin changes with clear mitigation.
- **HIGH:** gateway lifecycle, schema migration, auth/provider, Node requirement, or key channel impact.
- **BLOCKER:** target unavailable, environment requirement unmet, known bug affects critical path, or rollback cannot be made safe.

HIGH requires explicit explanation and confirmation. BLOCKER stops unless the user explicitly accepts risk and rollback limits.

**Plugin skew is directional.** A host-bound official plugin **newer** than the host is HIGH or BLOCKER: it forward-references SDK paths the older host lacks and will hard-crash at load. A plugin **older** than the host usually degrades or warns rather than crashing. Converged end-state: official plugins at the host version, pinned with an exact-version install.

### 5. Build Critical Path Checklist

Define what “usable” means for this user before upgrading. Include:

- Gateway process/connectivity.
- Config validity.
- Dashboard or local control access if used.
- Important channels, e.g. Feishu/Telegram/WhatsApp.
- Important agents and routes, e.g. main, CodingMeow/codex-peer.
- Model/provider/auth path used by those agents.
- Essential plugins/skills/memory/browser/search tools.

For ordinary users, show only a short plain-language summary.

### 6. Preflight Health

Check whether the system is healthy before upgrading. If it is already unhealthy, do not mix pre-existing failure with upgrade failure. Either fix preflight issues first or ask whether to continue with a degraded baseline.

### 7. Verified Backup Gate

Before any mutation, create a timestamped local backup directory, e.g.:

```text
~/.openclaw/backups/openclaw-upgrade/YYYYMMDD-HHMMSS/
```

Minimum backup manifest:

- `openclaw.json` or actual config path.
- Current CLI version and path.
- Gateway/service status and manager details.
- Service command/path and running process command line when available.
- Config validation result.
- Install/package metadata for the detected package manager.
- Installed versions of critical/official plugins, recorded alongside the host version so skew is visible.
- Critical path baseline results.
- Target version and risk review summary.

Backup must be read back and hash/manifest verified. If backup creation or read-back fails, stop.

Do not default to copying all `~/.openclaw`; it may contain secrets, logs, caches, sessions, and large/private data. Expand backup scope only when release review identifies state/data migration risk, and keep it local.

### 8. User Confirmation

🔴 CHECKPOINT: Before mutation, present a concise plan and wait for explicit approval:

```text
Current: ...
Target: ... (stable/latest/user-specified)
Risk: LOW/MEDIUM/HIGH/BLOCKER
Impact: gateway restart? estimated downtime?
Backup: verified at ...
Rollback: ask first / auto-rollback authorized
Critical paths to verify: ...
Proceed? yes/no
```

### 9. Execute Upgrade

Use only commands supported by the discovered command table and semantics review. Prefer official/current-version mechanisms. If a command fails because it is missing or its options changed, refresh help/docs once and adapt; do not keep trying remembered commands.

If the gateway blocks the update, use a safe path that preserves the old running system when possible, then restart/reload with the correct manager.

### 10. Restart or Reload

Do not assume restart completed. Verify:

- New process is running.
- Runtime path matches the upgraded installation.
- Service manager state is healthy.
- Gateway connectivity probe succeeds.

Respect OpenClaw lifecycle guidance: use restart rather than stop+start unless the user explicitly approved stop/start or the current version's docs require it.

### 11. Post-Upgrade Verification

Required checks:

- CLI/package version equals target.
- Running gateway/runtime version equals target, or explain why exact runtime version is unavailable and provide alternative evidence.
- Running process path matches upgraded path.
- Gateway status/connectivity healthy.
- Config validation/doctor equivalent passes.
- Logs have no fresh fatal startup errors.
- Critical plugins/channels/agents/routes from the checklist are available. For each `@openclaw/*` plugin, confirm its installed version matches the host; a plugin version **higher** than the host is a blocker, not a warning.
- For critical plugins (e.g. Codex), a runtime-level load probe is **required**, not optional: `plugins list` proves only cold-state discovery, not that the plugin loads at runtime. Use a real message-path or runtime-load probe whose command and meaning are confirmed against the current install's help/docs — do not hardcode a remembered plugin-inspect command.
- A minimal end-to-end check passes when safe and supported.

If rollback happens, run the same verification checklist after rollback.

## Failure Taxonomy and Retry Policy

Before any retry, refresh current state: CLI version/path, service status, config status, process path, and logs.

| Failure | Auto retry? | Action |
|---|---:|---|
| command not found / unknown option | once | Refresh help/docs, update command table, retry only adapted command |
| network timeout / registry fetch | 2-3 | Backoff, retry same idempotent fetch/install step |
| gateway starting / restart scheduled | 3-5 probes | Wait and recheck; do not claim restart complete early |
| gateway blocks update | once | Switch to safe upgrade path after state snapshot |
| CLI upgraded, gateway old | once | Restart/reload correct service manager, then double-check versions |
| plugin load / import / runtime failure | no | Suspect host↔plugin version skew first, then auth, then hook timeout; converge plugin to host. Do not blame Node/cache/OAuth before checking versions |
| config validation failed | no | Stop; restore config only with authorization or propose fix plan |
| permission denied / sudo needed | no | Stop and ask; do not escalate silently |
| auth/token/provider failure | no | Stop and ask user to refresh credentials |
| state/data migration risk or partial migration | no blind retry | Preserve evidence; rollback may be unsafe; ask before repair/rollback |
| post-upgrade unhealthy | limited | Collect logs; repair-forward or rollback only within prior authorization |

Never rerun the entire upgrade loop blindly. Never use destructive cleanup, reinstall, config overwrite, or version downgrade without explicit authorization.

Triage rule for plugin errors: **suspect version skew before Node, cache, or OAuth.** A plugin that fails to load is far more often newer than the host than it is missing a dependency.

## Final Report Format

For ordinary users:

```text
Upgrade result: success / failed / rolled back / stopped safely
From -> To: ... -> ...
Why this target: stable/latest/user-specified
Backup: verified at ...
Gateway: healthy/unhealthy
Critical paths: pass/fail/not checked
Rollback: not needed / completed / available / unsafe
Need your action: yes/no
```

For expert detail, include:

```text
CLI version/path: ...
Gateway version/path/process: ...
Service manager: ...
Config validation: ...
Release risk level: ...
Commands used: ...
Retries: ...
Logs checked: ...
Remaining risks: ...
```

## Evidence Table Template

Track phase evidence as the upgrade progresses. Every required phase should have a row before moving on:

```markdown
| Phase | Evidence source / command | Result | Blocker? | Next action |
|---|---|---|---|---|
| discover environment | <source> | <fact> | no | continue |
| command semantics | <help/doc/output> | <supported command + meaning> | no | continue |
| release risk review | <release notes/issues> | <risk level + reason> | no/yes | continue/stop |
| verified backup | <manifest/hash/read-back> | <verified path> | no | ask confirmation |
| post-upgrade verification | <status/log/check> | <pass/fail> | no/yes | report/repair/rollback |
```

If a row cannot be filled, stop and report the missing evidence instead of inferring success.

## Pressure Scenario Examples

### Scenario: latest requested but release risk is unclear

User says: "Upgrade OpenClaw to latest."

Expected behavior:

1. Discover current install, gateway manager, config path, and critical channels.
2. Verify the latest exact version and release notes.
3. If release evidence is missing or high-impact changes are unclear, recommend a stable target or stop with `unknown risk is not low risk`.
4. Ask for confirmation before mutation.

### Scenario: CLI upgraded but gateway still runs the old binary

Evidence:

- CLI/package version equals target.
- Running process command path still points to the old install.
- Gateway reports old runtime evidence or does not expose target evidence.

Expected behavior:

1. Do not claim success.
2. Record path mismatch in the evidence table.
3. Restart/reload the correct service manager only if authorized and supported.
4. Recheck process path, gateway connectivity, and critical routes.

### Scenario: upgrade succeeds but gateway is unhealthy

Expected behavior:

1. Collect fresh logs and status.
2. Classify failure before retry.
3. Repair-forward or rollback only within prior authorization.
4. If rollback occurs, run the same verification checklist after rollback.

### Scenario: host pinned to an older stable version, but an official plugin auto-updated ahead

Evidence:

- Host (CLI/package) is at the user-chosen stable version.
- An `@openclaw/*` plugin under `~/.openclaw/npm` is at a higher version than the host.
- A message fails with a plugin load error referencing a host SDK module path the older host does not provide.

Expected behavior:

1. In Discover Environment, record each official plugin's version and flag any plugin newer than the host.
2. Classify plugin-newer-than-host as HIGH or BLOCKER, not a warning.
3. Converge **toward the pinned target**: bring the plugin down to the host version with an exact-version install, rather than letting an auto-updated plugin pull the host up. This is `latest is not automatically best` applied to the plugin axis.
4. Re-run post-upgrade verification, including a runtime load probe for the affected plugin.

## Common Failure Modes This Skill Prevents

- Upgrading `which openclaw` while LaunchAgent keeps running a different binary.
- Claiming completion after package install without checking gateway runtime.
- Treating a scheduled restart as a completed restart.
- Assuming old commands/flags work on every OpenClaw version.
- Recommending latest when stable is safer.
- Skipping release notes and discovering breaking changes after the system is down.
- Having a backup that was never read back and cannot be restored.
- Retrying a partial upgrade until the original state is lost.
- Rolling back config/version without approval.
- Calling gateway healthy while Feishu, agent routes, models, memory, or plugins are broken.
- Treating the host version as proof of completion while an official plugin has drifted to a newer, incompatible version.

## GitHub Publishing Checklist

Before publishing this skill:

- Keep the skill self-contained; no secrets, local paths, or user-specific credentials.
- Test with pressure scenarios: rushed latest upgrade, version-sensitive commands, partial failure recovery.
- Verify frontmatter uses a discovery-focused description, not a workflow summary.
- Include examples only if they are generic and version-tolerant.
- Do not include commands that imply they are universal across OpenClaw versions.
