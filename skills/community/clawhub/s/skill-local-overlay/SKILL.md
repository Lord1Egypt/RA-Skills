---
name: skill-local-overlay
slug: skill-local-overlay
displayName: Skill Local Overlay
version: "1.0.6"
description: "Local patch layer for marketplace, connector, and built-in skills that get overwritten on platform or plugin upgrades. Use BEFORE modifying any skill that is not agent-created, and AFTER an upgrade that may have wiped local edits. Snapshot before edit, record every change in a patch ledger (补丁台账), replay patches after upstream upgrades. Trigger keywords: 修改内置 skill, marketplace skill 更新覆盖, upgrade overwrote my changes, skill 修改丢失, 升级覆盖本地修改, overlay patch, patch ledger, 补丁台账, connector skill 定制, builtin skill 修改, keep local edits, re-apply patches."
description_zh: "marketplace / connector / 内置 skill 的本地补丁层：改动前快照 + patch ledger 补丁台账 + 升级后重放。凡会被平台升级覆盖的 skill，本地修改一律走 overlay 目录 + 台账，不再裸改。改前必读。"
read_when: "About to modify a marketplace, connector, or builtin skill file, or after any platform or plugin upgrade that may have overwritten local patches."
not_for:
  - Agent-created skills (edit directly, they are owned locally)
  - Publishing skills to platforms (use skill-audit-publish)
  - Batch operations across many skills (use skill-batch-ops)
agent_created: true
---

# Skill Local Overlay

Purpose: stop losing local modifications when marketplace/connector/builtin skills upgrade. In-place edits to those layers are wiped by the next platform update. This skill wraps every change in snapshot → ledger → replay.

## Asset Layer Classification (do this first)

1. [Deterministic] Identify which layer the skill lives in:
   - **Agent-created** (frontmatter `agent_created: true`, user skills dir): owned locally → edit directly, no overlay needed.
   - **Marketplace-installed**: overwritten on reinstall/upgrade → overlay required.
   - **Connector skills**: overwritten when the connector updates → overlay required.
   - **Builtin / plugin cache** (versioned directories): overwritten on every plugin upgrade → overlay required.

## Workflow

1. [Deterministic] **Snapshot**: before touching anything, copy the original file(s) into the overlay directory with the upstream version recorded: `<overlay-root>/<skill-name>/<upstream-version>/<filename>.orig`. Standard overlay root: `~/.workbuddy/skills-overlays/`.
2. [Deterministic] **Ledger entry**: append one entry to `<overlay-root>/<skill-name>/ledger.md`:
   - date, upstream version, file path, what changed and why, snapshot location.
   - One entry per change. No batching multiple edits into one vague entry.
3. [Deterministic] **Apply the patch** to the live file. Keep patches minimal and additive where possible (small sed-able edits, not full-file rewrites) so they survive upstream drift.
4. [LLM] **Replay after upgrade**: when the upstream version changes, diff the new upstream file against the snapshot. Re-apply each ledger entry that still applies; report entries that no longer apply cleanly (upstream restructured) for a human decision.
5. [Deterministic] **Verify after replay**: re-run the diff; confirm every replayed patch is present exactly once in the live file (no duplicate application); update the ledger with the new upstream version.

## Hard Rules

- Never edit a marketplace/connector/builtin skill without a snapshot + ledger entry first.
- Never delete snapshots or ledger history.
- Replay must be idempotent: applying the same patch twice must not duplicate content.
- Patches stay minimal; if a "patch" grows beyond ~50 lines of change, raise it as a fork decision instead of a patch.
- Ledger entries record WHY, not just WHAT.
- The ledger is append-only: correcting a wrong entry adds a new entry that supersedes it. Never edit or delete history.
- Before replaying any overlay, diff the live file against its recorded ledger entry; a mismatch stops the replay and is reported, rather than being resolved by overwriting the live file.

## Failure Handling

- Snapshot copy fails (permissions, path issues): stop, do not edit. Report the exact path and error.
- Upstream upgrade changes a file so a patch no longer applies: keep the live file unpatched, mark the ledger entry STALE, and surface the conflict — never force-merge blindly.
- Overlay directory missing at replay time: treat as fresh start, re-snapshot, recreate the ledger, and note the gap.
- Live file contains edits not tracked in the ledger (drift): stop replay, surface the divergence to the user, and do not overwrite the live file until the drift is reconciled.

## Output Format

Report: layer classification → snapshot path → ledger entry ID → patch summary. After replay: per-entry status table (APPLIED / STALE / CONFLICT) + new upstream version.
