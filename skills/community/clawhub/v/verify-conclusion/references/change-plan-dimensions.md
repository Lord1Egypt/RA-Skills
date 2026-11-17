# Change-plan dimensions — 11-dimension baseline for upgrade / migration / refactor / cleanup plans

Use this list as the **Phase 0 baseline** (see SKILL.md Step 0) when the object under review is a plan
that another party will execute. Do not derive the dimension list from the document itself — that is what
makes absent dimensions invisible. Fill each row with a verdict (`covered` / **`absent`** / `n.a.`) and the
evidence you judged it from.

> Every threshold, duration and count below is a **historical measurement from one self-hosted host
> (2026)**. Re-measure before reusing a number; treat this file as a dimension list, not as settings.

| # | Dimension | What must be in the plan | Where the judgment comes from |
|---|---|---|---|
| 1 | **Code version & checkout model** | what the checkout is pinned to, whether the updater moves it itself, what "target version" actually resolves to (tag? channel? branch?), and what happens if a newer release lands before execution | updater source (`update_channel.*`, `update_cmd_git.*`), `git merge-base --is-ancestor`, release API `published_at` |
| 2 | **Dependencies & local patches** | packages present in the venv but absent from the lock (they get wiped), and every local patch with its re-apply anchor + test | `uv.lock` vs installed dist-info diff, `git diff --numstat`, patch doc |
| 3 | **Config migration & env rewrite** | which migration steps run, whether `.env` gets rewritten, which keys are touched, and whether each is a no-op for this host | migration source, `_config_version` on disk vs target table, `grep` of the host's own keys |
| 4 | **Data schema migration** | current schema version, target version, the DDL/DML it will run, whether rows are affected, and whether the *old* code can still read the migrated store on rollback | schema constants on both sides (`SCHEMA_VERSION`), migration body, a **real copy** of the store |
| 5 | **Scheduler / timed work** | which jobs fall inside the downtime window, each job's catch-up grace window, and whether a missed slot is retried once or skipped | scheduler source, per-job `grace_minutes`, global catch-up switch |
| 6 | **Service units & restart semantics** | whether the unit file is static or code-generated, whether the upgrade rewrites it, and whether `daemon-reload` / re-install is needed | unit path + generator source, `systemctl show`, update-flow greps |
| 7 | **Downstream consumers of names you change** | every script, skill, doc, cron prompt and config that references a renamed/removed tool, path or field | repo-wide search **including skills and cron prompts**, not just code |
| 8 | **Credentials & secrets** | what could be printed, logged, or copied by the change, and where plaintext copies land | secret-scan probe, secret-dir conventions, redaction coverage |
| 9 | **Rollback path & irreversibility** | the exact reverse steps, which steps are irreversible (data migration, deletions), and the cost of each | each mutation step, plus measured cost of the restore (not an estimate) |
| 10 | **Duration, space & resource budget** | worst-case wall-clock and disk, with the sampling conditions named (cold vs warm cache) | >=2 samples per figure, cache state named; else a range with the worst case |
| 11 | **Observation surface before/after** | what expected noise looks like (restart-time connection errors), what proves the new state is real, and which checks the CLI cannot perform | log excerpts from prior restarts, alternate verification path (in-process instead of CLI) |

## Extra rows for this host's stack

| # | Dimension | Note |
|---|---|---|
| 12 | **Long-lived tool artifacts vs isolation rehearsals** | a rehearsal root must live outside the data home if the package manager writes into the default root; otherwise it grades the wrong tree |
| 13 | **Checkers that load fewer extensions than the runtime** | e.g. a CLI lacking the runtime's FTS tokenizer reports "no such tokenizer" — that is a blind channel, not corruption |

## Worked example (2026-11-16, Hermes Agent v0.22.5 -> v0.23.1)

First review pass (Step 1 + Step 2 only) produced **3 corrections** and declared done. The coverage pass
produced **2 errors + 9 absent dimensions**, mapping to rows above: #4 schema (absent), #7 downstream
(readers of removed `browser_*` tool names, 9 skill files), #5 scheduler catch-up (absent), #6 unit
generation (absent), #10 duration with cache state (single sample reported as "measured"), #9 rollback
requirement (originally conditional; the schema migration made a DB restore mandatory), plus `.env`
rewrite, interpreter identity, and backup scope.

Lesson to keep: **9 of the 11 dimensions were absent from a plan that had already passed a chain attack
and a blind re-derivation.** Wrong-statement review is not a substitute for baseline coverage.
