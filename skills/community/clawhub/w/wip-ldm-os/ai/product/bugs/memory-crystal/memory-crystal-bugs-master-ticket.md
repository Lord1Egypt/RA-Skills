# Memory Crystal Bugs Master Ticket

**Date:** 2026-07-05
**Filed by:** cc-mini (Claude Code, Fable 5), with Parker
**Status:** open, master ticket
**Scope:** `ai/product/bugs/memory-crystal/`
**Open tickets:** [`open-tickets/`](open-tickets/)
**Closed tickets:** [`closed-tickets/`](closed-tickets/)
**Archive:** [`archive/`](archive/)
**Sibling master:** [`../openclaw/openclaw-master-ticket.md`](../openclaw/openclaw-master-ticket.md)

This is the rolling master ticket for Memory Crystal bugs. It owns triage order, the boundary with the OpenClaw harness folder, and rolling state. It is append-only: add entries, move status, add short editorial notes. Individual ticket files remain the source of truth for their own scope.

## Folder Standard

```text
ai/product/bugs/memory-crystal/
  memory-crystal-bugs-master-ticket.md
  open-tickets/
  closed-tickets/
  archive/
```

- `open-tickets/` contains active bugs that still need implementation, review, verification, or explicit disposition.
- `closed-tickets/` contains bugs that were fixed and should remain easy to find.
- `archive/` contains stale, superseded, or historical bug artifacts.

Do not leave loose bug tickets in the root. The root should contain only the master ticket and folders.

## Product Boundary

Memory Crystal is the cross-agent sovereign memory layer: the plugin + MCP server + CLI backed by `~/.ldm/memory/crystal.db`. Bugs belong here when they affect:

- capture (agent_end ingestion, chunking, embedding, skip-cursors, model-swap gaps);
- search (`crystal_search` quality, ranking, corpus coverage);
- the dual-memory architecture with OpenClaw native memory (routing, injection, engine/slot questions);
- Crystal's hooks, secrets/token plumbing, and resilience (billing failures, rotation, fail-fast);
- cross-harness use (Claude Code MCP, standalone CLI).

Boundary rules:

- **The dual-memory PARENT ticket lives here** (Crystal is the product; the harness is the venue). OpenClaw-side symptoms (gateway OOM, EMFILE, `main.sqlite` rot) file in `../openclaw/` and link back.
- Harness upgrade mechanics (fork, carries, canary, promotion) live in `../openclaw/` and `open-claw-upgrade-private`.
- The documentation gap (`how-memory-works.md`, stale `what-is-dotldm.md`) is tracked inside the parent ticket below until it graduates to its own docs PR.

## The Committed Architecture (context for every ticket here)

Decided 2026-06-25 (Parker + Codex review; UPDATE 2/3 of the parent ticket). Dual memory, both together, each in its lane:

- **Native OpenClaw memory-core stays the out-of-box default** and keeps local workspace/file search. Not gutted, not replaced.
- **Crystal supplements it as a Honcho-style `before_prompt_build` prompt-injection plugin**: relevant durable memory lands in the prompt each turn, before the agent decides to call any tool. No memory slot, no context-engine slot, no core fork.
- **QMD is not adopted.** It is MIT-licensed search-quality inspiration (hybrid search, reranking, query expansion; partially ported already). The `memory.backend` engine-swap framing is superseded history. Honcho's AGPL core service is not used; only the MIT plugin's injection pattern.
- **Two phases, separate PRs.** Phase 0: config-only stabilization (`fallback: "none"`, narrow `extraPaths`, `crystal_search` routing rule, archive the frozen 16GB `main.sqlite`). Phase 1: the injection hook with guardrails (token cap, top-K + confidence threshold, timeout + fail-open, provenance-as-quoted-reference, private-mode respect, idempotence).

## Active Bug Order

### P0: Dual-memory parent

1. [`open-tickets/2026-06-24--cc-mini--openclaw-native-memory-conflicts-with-crystal.md`](open-tickets/2026-06-24--cc-mini--openclaw-native-memory-conflicts-with-crystal.md) ... open, P1 severity, PARENT ticket. Read UPDATE 2 + UPDATE 3 first (committed direction, reconfirmed by Parker 2026-07-05) and UPDATE 4 (Phase 0 is now a blocking prerequisite for the OpenClaw v2026.6.11 upgrade, plus the CRYSTAL PROTECTION GATES: verified `crystal.db` backup + `crystal_search` round-trip from both Lēsa and Claude Code at three checkpoints... nothing may be lost). Sequencing owned by the recovery + upgrade umbrella in [`../openclaw/open-tickets/2026-07-04--cc-mini--lesa-noreply-loop-recovery-and-upgrade-plan.md`](../openclaw/open-tickets/2026-07-04--cc-mini--lesa-noreply-loop-recovery-and-upgrade-plan.md) (Track D, gate C0). Codex-review hardening 2026-07-05 (in UPDATE 4): the frozen `main.sqlite` gets a checksum-verified immutable canary copy BEFORE archiving, and the 72h no-EMFILE/no-OOM window blocks upgrade promotion (build/canary may overlap it). Note: the whole lane currently waits behind the openclaw umbrella's gate A0 (tracked-secret remediation).

### P1: Resilience and capture

2. [`open-tickets/2026-04-13--cc-mini--ship-plan-resilience-phases.md`](open-tickets/2026-04-13--cc-mini--ship-plan-resilience-phases.md) ... open. The 8-phase crystal-resilience plan from PR #585. Last known open item: **Phase 6a, OpenClaw format-error billing cooldown** (format errors must not cool down auth profiles or rotate sessions into amnesia). Verify remaining phases' status before picking up.
3. [`open-tickets/2026-04-12--cc-mini--crystal-ingestion-gaps-on-model-swap.md`](open-tickets/2026-04-12--cc-mini--crystal-ingestion-gaps-on-model-swap.md) ... open. Capture gaps when the harness swaps models mid-stream. Related to the resilience phases; check overlap before separate work.
4. [`open-tickets/2026-04-15--cc-mini--sa-token-env-and-hook-failfast.md`](open-tickets/2026-04-15--cc-mini--sa-token-env-and-hook-failfast.md) ... open. SA-token env plumbing + hooks must fail fast instead of silently. Verify against the current plugin before implementing; parts may have shipped with 0.7.x.

### Archived

Historical artifacts in [`archive/`](archive/): the 2026-04-01 memory-sync plan and memory-write hook notes (both superseded by the current capture architecture and the parent ticket).

## Operating Principles

1. **Append-only master.** Add entries and move status; do not rewrite history out of this file.
2. **Archive, never delete.** Indexes and DBs get archived after gateway-stop + coverage verification; ticket files get `git mv` to `archive/`.
3. **Crystal must stay cross-harness.** Standalone `crystal_search` (MCP/CLI) keeps working for Claude Code regardless of any OpenClaw integration work.
4. **Injection is guarded.** Any prompt-injection work enforces the Phase 1 guardrails, including treating recalled memory as quoted reference data, never as instructions (memory-poisoning defense).
5. **One slice per PR.** Phase 0 and Phase 1 of the parent ship separately; do not conflate config stabilization with plugin code.

## Co-authors

Co-Authored-By: Parker Todd Brooks <parkertoddbrooks@users.noreply.github.com>
Co-Authored-By: Lēsa <lesaai@icloud.com>
Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
