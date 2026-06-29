---
name: skill-build-wizard
description: >
  End-to-end guided workflow for building production-quality agent skills.
  Walks users through 4 stages: pre-flight checks → spec confirmation (3 musts) →
  coding quality acceptance (4 checks) → release prep (5 requirements). Use when
  the user says "create a skill", "build a skill", "write an agent skill",
  "skill-build-wizard", "做个 skill", "帮我创建一个 skill", "skill 全流程向导".
  Calls skill-creator for actual scaffolding and routes to glic-check /
  skill-release-audit / skill-release-plus / skill-regression for verification
  and release. Not for: just writing one quick skill file (use skill-creator
  directly); just publishing an already-finished skill (use skill-release-plus).
---

# skill-build-wizard — End-to-End Skill Building Workflow

- **Version**: 1.0.0
- **License**: MIT
- **Author**: Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)
- **Repository**: https://github.com/Songhonglei/build-better-skills
- **Part of**: [`build-better-skills`](https://github.com/Songhonglei/build-better-skills) suite — see [Stages](https://github.com/Songhonglei/build-better-skills#stages) for the lifecycle map.

A guided workflow that walks users through building production-quality agent skills.
Unlike `skill-creator` (a technical reference written **for AI**), this wizard is
written **for the user** — it sequences the work into 4 stages and pauses for
confirmation at each handoff so nothing important gets skipped.

## Usage

When a user says "build a skill" / "做个 skill" / "skill-build-wizard", execute the
four stages **in order**. Wait for user confirmation before advancing to the next stage.

---

## Stage 1: Pre-flight checks (skippable)

**Goal**: Make sure the workspace is ready, avoid rework later.

**Skip rules**: The user can skip this stage or any individual check at any time,
no explanation required.
- Skip all: user says "skip pre-flight" / "skip" / "no checks" → jump to Stage 2
- Skip specific: user says "skip git check" → skip just that item, run the rest
- On warnings/failures: report the result, then **proactively ask** "continue or
  fix first?" — never force a fix.

Run the pre-flight script (auto-locates the skill directory, supports `--skip`):

```bash
# Auto-locate the script (works under common locations)
SKILL_DIR=$(find "$HOME/.openclaw/workspace/skills" "$HOME/.claude/skills" /app/skills \
  -maxdepth 1 -name "skill-build-wizard" -type d 2>/dev/null | head -1)
bash "${SKILL_DIR}/scripts/pre-check.sh"

# Skip examples:
# bash "${SKILL_DIR}/scripts/pre-check.sh" --skip git
# bash "${SKILL_DIR}/scripts/pre-check.sh" --skip all
```

The script checks one thing and prints two general recommendations
(see `references/checklist-before-start.md`):

1. **Workspace Git** — version-track your work so you can undo any mis-edit
2. **(Recommendation)** Long-running task tolerance — ensure your agent/IDE
   won't time out mid-build
3. **(Recommendation)** Cross-session continuity — have a way to recover or
   reload the conversation context if it gets dropped

**Outcomes**:
- ✅ All pass → proceed to Stage 2
- ⚠️ Warning → tell the user, ask "continue or fix first?", honor their choice
- ❌ Failure → suggest a fix, ask "continue or fix first?", honor their choice

---

## Stage 2: Spec clarification → confirmation

**Goal**: Align on requirements and design **before writing any code**.

Three musts:

1. **Must use [`skill-creator`](https://github.com/anthropics/skills) for scaffolding** —
   say to the user: "I'll call skill-creator to build this skill", don't roll your own.
2. **Must give a complete design and wait for user confirmation before coding** —
   the design includes: skill purpose, directory structure, list of
   scripts/references/assets, trigger phrase design.
3. **Must avoid local dependencies** — no fixed paths (e.g. `/home/me/...`), no
   machine-specific env vars, no local DB endpoints.

**Question pacing** (ask in small batches, not a 10-question list):
- What problem does this skill solve? How will users trigger it?
- Can you give one or two concrete usage scenarios?
- Does the skill need external APIs or local file access?

**After the design is confirmed, before coding, optionally save the design**:
- Save to any markdown / docs system you use (your team wiki, Confluence,
  Notion, a local `DESIGN.md` file in the project, etc.) — this is optional
  and non-blocking.
- Document title: "[Skill name] — Design"
- Content: skill purpose, directory structure, scripts/references/assets list,
  trigger phrase design.
- If save fails or the user prefers not to save, proceed to coding directly
  (no need to block the flow).
- Tell the user: "Design confirmed. Starting code now; will run quality
  checks when done."

---

## Stage 3: Coding acceptance

**Goal**: Don't carry bugs into the release stage.

See `references/checklist-coding.md` for the full checklist. Run four checks
in order:

1. **Design alignment** — verify every functional point against the agreed design
2. **Edge cases** — empty input / API failure / file-not-found / dependency
   missing, etc.
3. **Code + doc review (2 passes)** —
   Pass 1: script stability (set -e traps, missing external commands, numeric
   guards, hardcoded paths, pipe safety) + SKILL.md doc quality (paths,
   fallback logic, references usage, trigger coverage);
   Pass 2: from the "first-time stranger user" perspective, walk the flow
   end-to-end and find dead ends.
4. **Smoke tests (2 passes)** — direct script run + end-to-end functional test,
   with real output as evidence.

**Gate**: All four must pass before advancing. Fix issues then re-run the
affected items.

**Before advancing to Stage 4, clean up build artifacts** (avoid shipping
temp files in the release package):
- Move any smoke-test scripts / logs / fixtures to a temp dir or delete them.
  Do **not** leave them in the skill directory.
- The skill directory should only contain release files: `SKILL.md`, `scripts/`,
  `references/`, `assets/`. No `*.log`, `*.bak`, `test_*` fixtures.
- Verify: `ls -la <skill-dir>` and confirm each file belongs.

---

## Stage 4: Release prep

**Goal**: Ship a clean, safe, cross-environment package.

See `references/checklist-release.md` for the full checklist. Five requirements,
**in this order**:

1. **[skill-regression](https://github.com/Songhonglei/build-better-skills/tree/main/skills/skill-regression)** — regression testing (fill in `Test.md`, then run twice)
2. **[glic-check](https://github.com/Songhonglei/build-better-skills/tree/main/skills/glic-check)** — 5-dimension quality review (Grammar / Logic / Integrity / Containment + Usability). The **Integrity** dimension catches dangerous writes, missing artifacts, and several security smells.
3. **[skill-release-audit](https://github.com/Songhonglei/build-better-skills/tree/main/skills/skill-release-audit)** — final mechanical gate before publish (SKILL.md spec, file structure, no stray README/CHANGELOG, etc.)
4. **Cross-environment validation** — install the package on a different machine
   or a teammate's environment, run from scratch. **Cannot be automated.**
5. **[skill-release-plus](https://github.com/Songhonglei/build-better-skills/tree/main/skills/skill-release-plus)** — sign, pack, and fan-out publish to one or more skill hubs.

**⚠️ Mandatory confirmation gate (prevents skipping acceptance)**:

Before executing step 5, you **must** confirm the following with the user
and wait for an explicit reply:

> "About to publish via **skill-release-plus**. Confirm:
> - Version: auto-bump / manually specified ___.___.___
> - Changelog: __________
>
> Reply 'confirm publish' to proceed."

**Absolutely forbidden**:
- ❌ Self-testing → commit → upload → publish in one shot. Before publishing,
  the user must see **a clear summary of changes + an acceptance report + a
  clickable preview URL** and explicitly accept.
- ❌ Publishing without confirmed version and changelog.

**After publish**: share the hub URL and ask the user to verify the skill name,
description, and version on the hub page.

---

## Dependencies

### System commands

- `git` — required for Stage 1 git check (recommended, not enforced)
- `python3` — optional, only used inside `scripts/pre-check.sh` for one minor
  detection; the script degrades gracefully if missing

### Skill dependencies

All four are part of the [`build-better-skills`](https://github.com/Songhonglei/build-better-skills) suite, plus `skill-creator` from upstream Anthropic skills:

- [`skill-creator`](https://github.com/anthropics/skills) — scaffolds the skill (called in Stage 2)
- [`skill-regression`](https://github.com/Songhonglei/build-better-skills/tree/main/skills/skill-regression) — Stage 4 Step 1
- [`glic-check`](https://github.com/Songhonglei/build-better-skills/tree/main/skills/glic-check) — Stage 4 Step 2
- [`skill-release-audit`](https://github.com/Songhonglei/build-better-skills/tree/main/skills/skill-release-audit) — Stage 4 Step 3
- [`skill-release-plus`](https://github.com/Songhonglei/build-better-skills/tree/main/skills/skill-release-plus) — Stage 4 Step 5

## Reference files

- `references/checklist-before-start.md` — Stage 1 details (3 pre-flight tips)
- `references/checklist-coding.md` — Stage 3 details (4 acceptance checks)
- `references/checklist-release.md` — Stage 4 details (5 release requirements)
- `scripts/pre-check.sh` — Stage 1 automated pre-flight script
