---
name: smart-updater
version: 1.1.0
changelog:
  - version: 1.1.0
    date: 2026-03-12
    changes:
      - "feat: SkillHub (腾讯国内镜像) integration — scan uses SkillHub index for batch version check (single request, no rate limit); upgrade downloads from SkillHub COS first, falls back to clawhub"
      - "perf: ClawHub skills in SkillHub top-50 are checked instantly without clawhub inspect calls"
      - "fix: scan result now includes inSkillHub flag for each clawhub update entry"
  - version: 1.0.0
    date: 2026-03-11
    changes:
      - "Initial release: inventory/scan/upgrade three-script system with Three Gates safety framework"
      - "Supports npm (core + extensions), ClawHub skills, GitHub-cloned skills"
      - "HITL mode: changelog analysis before any upgrade, user approval required"
description: "Intelligent upgrade management for OpenClaw skills, extensions, and core. HITL (Human-in-the-Loop) mode: scan installed assets, read changelogs, analyze risk, recommend upgrades, then execute only what the user approves. Use when: (1) user asks to check for updates or 检查升级, (2) user asks what's installed or 装了什么, (3) user wants to upgrade a specific skill/extension/plugin, (4) user mentions update/upgrade/版本/新版本, (5) periodic upgrade check via cron. Covers npm packages, ClawHub skills, GitHub-cloned skills, and OpenClaw core."
---

# Smart Updater

**Principle: 宁可不升，不可升坏。**

## Execution Contract

A final report is **invalid** unless ALL of the following are true:
- `inventory.json` exists (Phase 1 complete)
- `scan-result.json` exists (Phase 2 complete)
- Every update candidate has a changelog summary or explicit "unavailable" note (Phase 3 complete)
- Every update candidate has a risk level (Phase 4 complete)

If any condition is not met, do NOT generate the report. Output `BLOCKED` with the missing items instead.

### Never Do This
- Never generate the report before changelog fetch
- Never infer or invent changelog contents — fetch them
- Never present updates to the user without changelog evidence
- Never skip an update candidate in the report because its changelog was hard to find

---

## Quick Commands

### Inventory only
```bash
bash ~/.openclaw/workspace/skills/smart-updater/scripts/inventory.sh
```
Scans all installed assets → `~/.openclaw/inventory.json`

### Scan only
```bash
bash ~/.openclaw/workspace/skills/smart-updater/scripts/scan.sh
```
Checks each trackable asset for updates → `~/.openclaw/scan-result.json`

### Full Check (most common)
Execute Phases 1–5 below in order.

---

## Workflow

### Phase 1 — Inventory
**Action**: Run `inventory.sh`
**Output**: `~/.openclaw/inventory.json`
**Exit criteria**: File exists and contains `assets` array

Asset types: `core/npm`, `extension/npm`, `extension/local`, `extension/github`, `skill/clawhub`, `skill/github`, `skill/local`, `builtin/bundled`

Do not continue until Phase 1 exit criteria are met.

### Phase 2 — Scan
**Action**: Run `scan.sh`
**Output**: `~/.openclaw/scan-result.json`
**Exit criteria**: File exists and contains `updates` array

Do not continue until Phase 2 exit criteria are met.

If `updates` is empty → report "all up to date" and stop. No further phases needed.

### Phase 3 — Changelog Fetch
**Action**: For EACH update in `scan-result.json`, fetch changelog/release notes.
**Output**: Changelog summary per update candidate.

| Source | How to fetch |
|--------|-------------|
| **ClawHub** | `clawhub inspect <slug> --versions --limit 5` |
| **npm** | `npm info <pkg> --json` → check `repository`, then `web_fetch` GitHub releases |
| **GitHub** | `cd <dir> && git log --oneline HEAD..origin/main` or `changelogUrl` from scan-result |

Note: scan-result.json may already contain a `changelog` array for ClawHub skills. Use it if present, but verify/supplement if sparse.

**For each update, record:**
- One-line summary of what changed
- Source URL or command used
- Breaking changes (if any)
- "unavailable" with reason (if fetch failed)

**Exit criteria**: Every update candidate has EITHER:
- a changelog summary with source, OR
- an explicit "changelog unavailable" note with the source attempted

⛔ Do not continue to Phase 4 until Phase 3 exit criteria are met.

### Phase 4 — Risk Assessment
**Action**: Assign risk level to each update using this matrix:

| Condition | Risk | Action |
|-----------|------|--------|
| patch + bugfix | 🟢 Low | Recommend |
| minor + feature | 🟡 Medium | Suggest |
| major + breaking | 🔴 High | Require confirmation |
| extension type | 🟡+ | Always full Gate 2 flow |
| changelog unavailable | 🟠 Unknown | Flag for manual review |
| new executable scripts | 🟠+ | Suggest skill-vetter |
| name conflict | 🔴 | Block upgrade (Gate 1) |

**Exit criteria**: Every update candidate has a risk level assigned.

### Gate — Pre-Report Verification
Before generating the report, verify:
- [ ] Every update has changelog summary or "unavailable" note
- [ ] Every update has risk level
- [ ] Every update has changelog source (URL or command)

If ANY checkbox fails → output `BLOCKED: <missing items>`. Do NOT proceed.

### Phase 5 — Report
**Only now** read `references/report-format.md` and generate the report using that template.
The report MUST include changelog summaries from Phase 3. If Phase 3 data is absent, return to Phase 3.

### Phase 6 — Wait for User
Present the report and wait. Do NOT auto-upgrade. Do NOT proceed without explicit user selection.

---

## Upgrade Execution

When the user selects updates to apply:

**Execute upgrades one at a time, sequentially.** Each must pass Three Gates:

```
Gate 1: Pre-flight → Gate 2: Isolation → Gate 3: Post-flight → ✅
   fail↓                 fail↓                fail↓
  阻止升级             中止+回滚           回滚+通知
```

- **Gate 1**: Source tracked, no name conflict, gateway healthy (extensions), local/github extensions blocked
- **Gate 2**: Backup isolated, jiti cleared (extensions), config preserved (core), upgrade executed
- **Gate 3**: Version verified, file count checked, provenance validated, rollback on failure

**For detailed gate definitions and rollback procedures**: Read `references/three-gates.md`

For each upgrade: Announce → Gate 1 → Gate 2 (backup+execute) → Gate 3 (verify) → Report result

---

## Files

| File | Purpose |
|------|---------|
| `~/.openclaw/inventory.json` | Asset inventory (Phase 1) |
| `~/.openclaw/scan-result.json` | Scan results with changelog data (Phase 2) |
| `references/report-format.md` | Report template (Phase 5 only) |
| `references/three-gates.md` | Detailed gate definitions |
| `~/.openclaw/skill-backups/` | Skill backup directory |
| `~/.openclaw/extensions-backup/` | Extension backup directory |
| `~/.openclaw/plist-backup/` | Gateway plist backup (core upgrades) |
