---
name: version-decide
slug: version-decide
version: 1.1.0
displayName: Version Decider
summary: Decides the next SemVer version number from code changes, for beginner developers. Outputs a single, unambiguous version recommendation.
tags: [versioning, semver, semantic-versioning, release-decision, version-management, 版本号, 语义化版本]
description: 'Decide the NEXT SemVer version number from the SCOPE OF CODE CHANGES for an upcoming release, and output a single, unambiguous recommendation with cited standard clauses. Use only when the user is deciding which version to assign to a release they are about to cut (e.g. "what version should this release be", "major or minor or patch", "what to bump in 0.x", "how to advance alpha/beta/rc", "is this breaking"). NOT for: looking up an already-published version, asking the install command, CalVer/date-based versioning, or general release/project-management questions. Ships a deterministic arithmetic core: same input always yields the same output.'
when_to_use: |
  Typical triggers: "Next release adds a new character and a new feature — what version should it be?"
  "1.2.3 — which version fits next?"
  "0.3.1 — minor or patch?"
  Explicitly NOT for (do not mis-trigger):
  - CalVer / date-based versioning (version IS the release date, e.g. 26.04, 2026.08.19) — confirm the scheme before anything else
  - Only asking "when was v1.5.0 released" — that is a lookup, not a release decision
  - Asking the install command "how do I install v2" — that is package management, not version decision
  - Asking what the current version of some project is — just read it, this skill is not needed
  - Generic "should I release now" / project-management or roadmap questions — that is release planning, not version numbering
# Read/Grep/Glob: read-only version-file discovery. AskUserQuestion: confirm breaking-change
# ambiguity. Bash(python*) is scoped to running THIS skill's own scripts (semver_check.py) and
# read-only discovery commands (cat/grep/git tag); it is NOT granted for writes, network, or
# package management.
allowed-tools: Read, Grep, Glob, Bash(python*), AskUserQuestion
disable-model-invocation: false
user-invocable: true
metadata:
  openclaw:
    requires:
      bins: [python3]
      # Read-only locale variables consumed by scripts/semver_check.py for output-language
      # selection only (falls back to "en"). No secrets, no network config, no writes.
      envVars: [LC_ALL, LC_MESSAGES, LANG]
---

# Version Decider

Give developers (especially beginners) a **single, unambiguous** version-number recommendation, with the reasoning behind it.

---

## ⚠️ Cross-cutting hard constraints (must hold every turn; do not drop them under context compression)

> These 5 rules apply in **every** turn of the conversation. If this section is no longer visible in context, re-read this file.

1. **Never assume a breaking change on the user's behalf.** A version number's entire purpose is a compatibility promise to dependents; one wrong guess costs downstream production incidents. Whenever "is it breaking?" is in doubt, ask.
2. **Never guess the current version.** Always look it up from the project first (see Step 1). If you can't find it, ask. Never assume it starts at 1.0.0 or 0.0.1.
3. **Give exactly one version recommendation.** If two reasonable options exist, name the primary one and state the precondition for the alternative — never list several and make the user pick.
4. **Justify with the specific change + the standard's clause number** (e.g. SemVer §8). Never substitute empty phrases like "because it's a big change" for reasoning.
5. **Let the script do the arithmetic.** Always compute the version with `scripts/semver_check.py`; never do it by hand. If the script fails, show the raw error to the user verbatim — never fabricate a version number.

---

## Language

- This skill's `SKILL.md` and `references/` are **English by default** (ClawHub Natural Language Policy: English default).
- All **user-facing output follows the user's language**: if the user writes in Chinese, reply in Chinese.
- The CLI core `scripts/semver_check.py` localizes its `reasons` / error messages / level descriptions via `--lang en|zh|auto`. `auto` detects `LC_ALL`/`LC_MESSAGES`/`LANG` and falls back to `en`. JSON keys (`current`/`next`/`level`/...) stay English; values follow `--lang`.
- JSON **reports/logs** remain English only (per the policy's "JSON logs & reports English only" rule).

---

## Capabilities & safety boundaries

- **Decision engine:** `scripts/semver_check.py` (zero-dependency Python) computes every version via deterministic arithmetic. The model must never compute a version by hand; if the script errors, show the raw error and ask, do not fabricate a number.
- **Dev-only helpers:** `scripts/measure_skill.py` (SKILL.md compliance metrics) and `scripts/test_semver_check.py` (regression tests) are **maintenance tools**, not part of the runtime decision flow. They are never invoked to answer a release-decision question.
- **Locale only:** the engine reads **only** the `LC_ALL` / `LC_MESSAGES` / `LANG` environment variables, and only to choose output language. It does **not** read secrets, network configuration, or any other environment data.
- **No side effects / no privileges granted:** read-only inspection of local version files (e.g. `package.json`, `pyproject.toml`, `git tag`). No package installation, no repository mutation, no file deletion, no network calls. The declared tools are used **solely** for version discovery and running this skill's own scripts; this skill does not grant — and you should not grant — write, network, or package-management permissions on its behalf.


---

## Execution flow (5 steps, closed in a single turn)

One execution = Step 1 → 5. Each step has its own fallback; **never skip a step, and never rely on a later turn to re-read this file.**

### Step 1 — Collect 4 groups of inputs

| Input | How to get it | Fallback when missing |
|---|---|---|
| Current version | Inspect the project (commands below) | **Ask**: "Which version is currently released?" |
| Public API boundary | Library: read exports. App: ask "what is used externally" | If never declared → tell the user "define the public API first"; give no number this round |
| Change list + breaking? | Use AskUserQuestion or ask directly | If the user is vague → **ask concrete questions one by one**; never assume "probably not breaking" |
| Target ecosystem / channel | Ask | If the user doesn't care → assume npm semantics, but **state this assumption in the output** |

Commands to find the version (by priority):

```bash
cat package.json 2>/dev/null | grep '"version"'          # npm / Node
cat pyproject.toml 2>/dev/null | grep -i version          # Python
grep -m1 '^VERSION' Makefile 2>/dev/null                  # C/C++
git tag --sort=-v:refname 2>/dev/null | head -5           # git tag
grep -rnoE "v[0-9]+\.[0-9]+\.[0-9]+" --include=*.md . | head   # version comments / docs
```

**Six breaking-change checks (ask each; never default to "not breaking"):**
① Public export removed/renamed? ② Function signature changed (params added/removed/reordered/typed/returned)? ③ **Does a previously-successful call now fail or throw?** ④ Config/env/CLI arg/default changed? ⑤ Minimum dependency version raised? ⑥ Type or field narrowed?

Item ⑥ is the easiest to miss — narrowing generics or input types is breaking even if it still compiles.
Item ③ is the easiest to understate — semantic change is sneakier than a signature change.

**⛔ If Step 1 reveals the project is CalVer** (major segment ≥ 20 and looks like a year, e.g. `26.04`): stop and tell the user this skill does not apply; do not force SemVer rules on it.

### Step 2 — Grade the change

| Change | Level |
|---|---|
| Remove/rename public export, signature change, behavior change, config change, module deletion | **major** |
| Deprecate (still usable), add public API, relax dependency constraint | **minor** |
| Internal refactor, perf (behavior preserved), bug fix, security fix (no API change) | **patch** |
| Docs / tests / CI / formatting only | **none** (no release) |

Same batch is graded by **major > minor > patch precedence**: `feat + fix` → minor; `feat + break` → major.
Deprecation must be minor (SemVer §7 mandates it), even before removal.
Full table and gray zones: `references/decision-tables.md`.

**Fallback**: if unsure whether something is breaking → grade it major and state "if confirmed not breaking, downgrade to minor", handing the decision back to the user rather than assuming the optimistic case.

### Step 3 — Compute

```bash
python scripts/semver_check.py analyze <current> --changes "change1" "change2" ...
```

Change-spec syntax (the actual format of `scripts/semver_check.py`):

| Form | Level |
|---|---|
| `feat: add JSON output` / `feature:` | minor |
| `fix:` / `bugfix:` / `perf:` / `security:` / `refactor:` | patch |
| `docs:` / `test:` / `ci:` / `chore:` / `style:` / `build:` | none |
| `deprecate: mark old API deprecated` | minor |
| `revert: revert style tweak` | patch |
| `revertbreak: undo 2.0 field rename` | major |
| `break: parse() arg order changed` | **forces major** |
| `feat@break: swap the underlying driver` | **forces major** |

Flags: `--pre alpha|beta|rc` (open/advance pre-release) | `--pre alpha.2` (explicit sequence) | `--build 20261008.a1` (build metadata, no precedence effect) | `--rebase` (target a different version number within a pre-release line)

Other subcommands: `check <ver>` (validate + ecosystem hints) | `next <ver> --level <lvl>` (`lvl` includes `stable` for 0.x graduation) | `explain` (reasoning chain only) | `compare a b` (precedence)

Add `--lang en|zh|auto` to any subcommand to localize the output.

**Fallback**: if the script errors, show the raw error and fix the input per the message — **never** bypass the script and compute by hand (that is exactly the uncertainty this skill removes).

### Step 4 — Output

Fixed four-part form: conclusion → reasoning → to confirm → next command.

```
Version recommendation: 1.3.3 -> 1.4.0

Decision: minor (backward-compatible new feature)

Reasoning:
- Add character Yang Tinghe -> new content, backward-compatible, minor (SemVer §7)
- Add achievement system -> same
- By major > minor > patch precedence -> minor, patch reset to zero

Need your confirmation:
- Does the new achievement reuse the existing localStorage key? (reuse would corrupt old players' progress and may be breaking)

Next step:
- python scripts/semver_check.py next 1.4.0 --level minor
```

Unconfirmed gray zones (security fix, perf refactor, raised env requirement, save-format change) **must be called out**; see §4 of `references/decision-tables.md`.

### Step 5 — Wrap up

- If the conclusion depends on an unconfirmed assumption → list it under "Assumptions this round" at the end.
- If the user asks for the basis → cite the standard text in `references/standards-comparison.md`; don't re-repeat this file.
- If the decision is stuck on a human-approval action like 0.x graduation → state clearly "this needs you to confirm the API is frozen; I can't decide it for you".

---

## Quick reference — high-frequency scenarios

| Situation | Conclusion |
|---|---|
| **0.x stage** | Use npm/Cargo semantics: **a minor bump IS the breaking boundary** (`^0.2.3` caps at `0.3.0`). So `0.3.1` + feature → `0.4.0`, not `0.3.2` |
| **0.x → 1.0.0** | Not auto-derived. It is the explicit graduation action `--level stable`, meaning "API is stable from now on"; a human must confirm the API is frozen |
| **Within a pre-release line** | core unchanged (SemVer §9: pre-release not guaranteed to satisfy the normal version's compatibility) → keep breaking during alpha **without** raising major. Only alpha→beta→rc→stable, step by step; skipping is rejected by the script |
| **Revert a non-breaking change** | patch |
| **Revert a breaking change** | **major** — compatibility is broken a second time; dependents just recovered and are broken again |
| **Deprecate an API** | minor (spec-mandated); major when actually removed. Gives downstream a minor cycle as migration window |
| **Edit README / comments** | no release needed |
| **Change an already-published version** | forbidden (§3); only release a new version |
| **Coexist multiple majors** | Go v2+ must change the module path (`/v2`); npm uses dist-tag (`next`/`beta`); Python relies on virtualenvs; Rust resolves multiple versions under one package name |

### Beyond SemVer

- **Python (PEP 440)**: pre-releases have **no hyphen** — `1.0.0rc1`, not `1.0.0-rc.1`. `check` detects this. epoch (`1!1.0`) only when switching numbering schemes.
- **CalVer**: see the ⛔ in Step 1; not applicable to this skill.

---

## Files

| File | Purpose | When to read |
|---|---|---|
| `references/decision-tables.md` (EN) / `decision-tables.zh.md` | Full decision table, confirmation checklist, edge cases, gray zones | when a grading is unclear |
| `references/standards-comparison.md` (EN) / `standards-comparison.zh.md` | SemVer / Conventional Commits / PEP 440 / Cargo / Go / CalVer official text and conflicts | when the user asks for the basis |
| `references/i18n-plan.md` | i18n implementation plan (ClawHub NL-policy compliance) | when changing languages/structure |
| `scripts/semver_check.py` | Decision arithmetic core (zero-dependency) | required in Step 3 |
| `scripts/test_semver_check.py` | 37 regression tests | after editing the script |
| `scripts/measure_skill.py` | Measures this file's compliance metrics | after editing this file |
| `locales/en.json` / `locales/zh.json` | User-facing copy tables | when adding/changing messages |
