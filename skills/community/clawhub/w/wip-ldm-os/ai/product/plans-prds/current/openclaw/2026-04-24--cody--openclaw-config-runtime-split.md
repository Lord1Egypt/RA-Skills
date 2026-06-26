# Plan: OpenClaw Config Runtime Split

**Date:** 2026-04-24
**Author:** Cody, with Parker
**Status:** plan
**Related:**
- `ai/product/plans-prds/current/memory-crystal/2026-04-24--cody--memory-audit-ledger.md`
- `ai/product/plans-prds/current/ldmos-core/2026-04-24--cody--runtime-config-audit-boundaries-ticket.md`
- `ai/product/bugs/memory-crystal/2026-04-24--cc-mini--unified-reliability-triage.md`

## Problem

OpenClaw is designed to use `~/.openclaw` as a mutable app home. That is normal. It contains config, sessions, auth state, memory DBs, extension state, logs, locks, and temp files.

The failure mode appears when the whole `~/.openclaw` directory is treated as a source-of-truth git repo. Runtime files then become candidates for commits, PRs, branch switches, and merges. On April 24, the deployed tree mixed legitimate config commits with auth/session/runtime state and SQLite temp files. That blocked a clean config deployment and created risk of publishing private runtime state to `origin/main`.

## Principle

OpenClaw owns its runtime home. LDM OS owns declarative desired state. Git tracks config intent and manifests, not raw runtime.

## Goals

1. Keep OpenClaw's runtime layout compatible with upstream.
2. Stop using the full `~/.openclaw` tree as the development source of truth.
3. Track only declarative OpenClaw config and install metadata in git.
4. Keep runtime memory, sessions, auth, logs, locks, temp files, and extension state out of source history.
5. Provide a safe deployment path from config repo to `~/.openclaw`.

## Non-goals

- Do not ask OpenClaw upstream to reorganize its home directory before we can fix our workflow.
- Do not move raw DBs or sessions into git.
- Do not make Parker manually edit deployed JSON as the merge strategy.

## Proposed split

### Config source repo

Track desired state only:

```text
openclaw/
  openclaw.json
  launchd/
    ai.openclaw.gateway.plist.template
  plugins/
    allowlist.json
    versions.json
  runbooks/
    upgrade.md
    rollback.md
  manifests/
    runtime-manifest.example.json
```

### Runtime home

Remain mutable and mostly untracked:

```text
~/.openclaw/
  openclaw.json                  deployed from config source
  agents/**/sessions/**          runtime
  agents/**/agent/auth-state.json runtime sensitive
  memory/*.sqlite*               runtime DBs and temp files
  memory/*.jsonl                 runtime logs/metrics
  logs/**                        runtime logs
  extensions/**                  installed artifacts
  workspace/**                   identity/workspace surface
```

## Git boundary

Allowed in config git:

- `openclaw.json`
- plugin allowlist and version manifests
- launchd templates
- upgrade and rollback runbooks
- redacted runtime manifests

Never allowed in config git:

- `agents/**/sessions/**`
- `agents/**/agent/auth-state.json`
- `memory/*.sqlite`
- `memory/*.sqlite-*`
- `memory/*.tmp-*`
- `memory/*.jsonl`
- logs
- lock files
- `.worktrees/**`
- extension build outputs unless intentionally vendored

## Deployment flow

1. Agent edits declarative config in the config repo worktree.
2. PR review merges config change.
3. Installer or deploy command copies approved config into `~/.openclaw`.
4. Deploy command snapshots current runtime metadata before restart.
5. Gateway restarts only after config validation passes.
6. Runtime audit manifest records what changed.

The deploy command should be idempotent and should never require Parker to be the merge tool.

## Runtime manifest

OpenClaw runtime gets a git-safe manifest similar to Memory Crystal's audit manifest:

```json
{
  "time": "2026-04-24T18:30:00Z",
  "openclaw_version": "2026.4.23",
  "config_hash": "sha256:...",
  "launchd_plist_hash": "sha256:...",
  "plugins": {
    "memory-core": "bundled",
    "memory-crystal": "0.7.36-alpha.1"
  },
  "runtime_sizes": {
    "main.sqlite": "16GB",
    "sessions_dir": "304MB"
  },
  "state_counts": {
    "session_files": 1131,
    "sqlite_tmp_files": 0
  }
}
```

This manifest is audit metadata, not raw memory.

## Guardrails

- `git diff --name-only origin/main...HEAD` must be clean of runtime paths before any config PR.
- Branch guard should block commits that include auth/session/memory DB paths.
- `ldm doctor` should warn if `~/.openclaw` is a git repo with tracked runtime files.
- Deploy should refuse to overwrite `openclaw.json` if the runtime config has uncommitted user edits not present in the source config, unless an operator explicitly chooses a reconciliation path.

## Phases

### Phase 1: Document and ignore runtime paths

- Add a clear `.gitignore` template for any existing dot-openclaw config repo.
- Remove tracked runtime files from index with `git rm --cached`, not from disk.
- Add `ldm doctor` warning for tracked runtime files.

### Phase 2: Config source extraction

- Establish the canonical config repo/path.
- Move current intended `openclaw.json` into that source.
- Keep runtime `~/.openclaw/openclaw.json` as deployed output.

### Phase 3: Deploy command

- Add `ldm openclaw deploy-config` or equivalent.
- Validate JSON.
- Write backup of deployed config.
- Copy config.
- Emit runtime manifest.

### Phase 4: Audit integration

- Add daily runtime manifests.
- Track config hash, plugin versions, DB sizes, session counts, and temp-file counts.
- Do not track raw DBs, sessions, auth state, or logs.

## Acceptance criteria

- A model/config change can be PR'd without including runtime files.
- A deploy can activate `openclaw.json` without branch switching inside `~/.openclaw`.
- `ldm doctor` flags tracked runtime files.
- A daily manifest can prove which config and plugin versions were active.
- Raw runtime files remain outside git.
