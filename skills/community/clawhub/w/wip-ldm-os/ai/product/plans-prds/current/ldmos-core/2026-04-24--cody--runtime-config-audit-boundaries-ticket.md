# Ticket: Runtime, Config, and Memory Audit Boundaries

**Date:** 2026-04-24
**Author:** Cody, with Parker
**Status:** ticket
**Repo:** wip-ldm-os-private
**Related:**
- `ai/product/plans-prds/current/memory-crystal/2026-04-24--cody--memory-audit-ledger.md`
- `ai/product/plans-prds/current/openclaw/2026-04-24--cody--openclaw-config-runtime-split.md`
- `ai/product/bugs/memory-crystal/2026-04-24--cc-mini--unified-reliability-triage.md`

## Summary

Create a formal LDM OS boundary between declarative config, mutable runtime state, and audit metadata.

The April 24 OpenClaw reliability work exposed a structural problem: `~/.openclaw` is a mutable app home, but it has been used like a source-of-truth repo. That allowed runtime files, auth/session state, memory DB temp files, and legitimate config commits to mix in one branch. The same risk applies anywhere LDM OS tracks raw runtime directories directly.

LDM OS needs a general rule and tooling:

> Git tracks intent and manifests. Runtime stores data. Audit ledgers track provenance and integrity. Backups preserve recoverability.

## Product decision

LDM OS should not git-track raw memory or harness runtime state.

Instead:

1. Config repos track desired system state.
2. Runtime stores keep private mutable data.
3. Audit ledgers record hashes, counts, provenance, and status.
4. Encrypted backups preserve recoverability.

## Scope

This ticket coordinates the Memory Crystal and OpenClaw plans:

| Product | Plan | Responsibility |
|---|---|---|
| Memory Crystal | Memory audit ledger | Prove capture and ingestion without committing `crystal.db` |
| OpenClaw | Config/runtime split | Stop committing app-home runtime state while keeping config deployable |
| LDM OS | This ticket | Installer, doctor, guard, manifest, and deployment conventions |

## Required LDM OS work

### 1. Runtime path classification

Add a shared classification table for paths:

| Class | Git policy | Examples |
|---|---|---|
| Config intent | track | `openclaw.json`, plugin versions, launchd templates |
| Runtime private | never track | sessions, auth state, memory DBs, logs, locks |
| Audit metadata | track if redacted | manifests, schema hashes, table counts, content hashes |
| Backup artifact | encrypted only | raw DB backups, raw session archives |

This classification should be available to `ldm doctor`, branch guard, and installer/deploy commands.

### 2. `ldm doctor` checks

Add checks for:

- `~/.openclaw` or `~/.ldm` git repos with tracked runtime files.
- tracked `*.sqlite`, `*.sqlite-*`, `*.tmp-*`, `auth-state.json`, session JSONL, logs, and locks.
- untracked but large runtime files inside config source repos.
- config repos missing a runtime `.gitignore` template.

Doctor should report the issue and suggest `git rm --cached`, not deletion.

### 3. Config deploy command

Add or specify a deploy path for OpenClaw config:

```bash
ldm openclaw deploy-config
```

Responsibilities:

- read config from source repo,
- validate JSON,
- snapshot current deployed config,
- copy to `~/.openclaw/openclaw.json`,
- write an audit manifest,
- optionally restart gateway after explicit confirmation or caller flag.

### 4. Audit manifest command

Add:

```bash
ldm audit manifest
ldm audit verify
```

Initial manifest scope:

- config hashes,
- plugin versions,
- DB sizes,
- table counts where safe,
- session file counts,
- temp-file counts,
- Memory Crystal ingest status totals.

No raw text, raw sessions, embeddings, secrets, or DB contents.

### 5. Branch guard integration

Branch guard should block commits or PRs that include runtime-private paths unless an explicit allowlist says the repo intentionally tracks them.

Blocked examples:

- `agents/main/agent/auth-state.json`
- `agents/main/sessions/*.jsonl`
- `memory/*.sqlite`
- `memory/*.sqlite-*`
- `memory/*.tmp-*`
- `logs/**`

### 6. Backup story

Document encrypted backups for raw memory:

- raw DBs and sessions go to encrypted backup storage,
- git receives only manifests and hashes,
- restore flow verifies restored DB against manifests where possible.

## Deliverables

1. Path classification spec in LDM OS docs.
2. `ldm doctor` runtime-tracking warnings.
3. OpenClaw config deploy command or documented deploy convention.
4. Memory Crystal audit ledger spec wired into Memory Crystal plan.
5. Git-safe daily manifest format.
6. Branch guard runtime-path blocklist.
7. Backup and restore documentation.

## Acceptance criteria

- A future OpenClaw config change can be PR'd without including runtime state.
- `ldm doctor` catches a repo that has tracked `auth-state.json`, sessions, or SQLite temp files.
- Memory Crystal can prove a conversation was captured without committing raw text.
- Daily manifests can be committed safely.
- Raw memory DBs and sessions are backed up encrypted, not tracked in git.

## Open questions

1. Where should the canonical OpenClaw config source live long term: LDM OS repo, dot-openclaw private repo, or a dedicated config repo?
2. Should audit manifests live in `~/.ldm/manifests/`, the private LDM OS repo, or both?
3. Which backup target becomes canonical for raw memory: local encrypted archive, object storage, or both?
4. Should branch guard enforce runtime-path blocks globally or only for known harness home repos?
