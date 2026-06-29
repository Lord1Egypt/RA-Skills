# Release prep: 5 requirements

Before packaging and publishing, complete these five requirements in order.
Each one exists for a reason — don't skip.

## Requirement 1 — Regression testing

Use [skill-regression](https://github.com/Songhonglei/build-better-skills/tree/main/skills/skill-regression) for functional regression:

```
Invoke skill-regression → point it at your skill directory
```

- After the first run, expand the generated `Test.md` with additional cases
  (especially edge cases)
- Run again, ensure all tests pass
- Only proceed to Requirement 2 once everything is green

---

## Requirement 2 — Quality review (5-dimension)

Use [glic-check](https://github.com/Songhonglei/build-better-skills/tree/main/skills/glic-check) for a 5-dimension quality review:

```
Invoke glic-check → point it at your skill directory
```

Dimensions: **G**rammar / **L**ogic / **I**ntegrity / **C**ontainment + **U**sability.

The **Integrity** dimension catches:
- Hardcoded secrets / tokens / API keys
- Dangerous shell patterns
- Missing safety guards on writes / deletes
- Cleanup gaps that would ship test fixtures

Any **ERR** findings must be fixed before publish. **WARN** findings: fix unless
you have an explicit reason to keep them (which should be documented in
SKILL.md).

---

## Requirement 3 — Pre-publish audit

Use [skill-release-audit](https://github.com/Songhonglei/build-better-skills/tree/main/skills/skill-release-audit) — the final mechanical gate:

```
Invoke skill-release-audit → point it at your skill directory
```

Audit covers: SKILL.md spec compliance, description quality, file structure,
no stray files (README/CHANGELOG/USAGE duplicates, etc.).

Auto-fix what's fixable. Manually fix the rest, then re-audit until clean.

---

## Requirement 4 — Cross-environment validation

**Install your `.skill` package on a different machine, or on a teammate's
agent environment, and run the main flow from scratch.**

- Confirm no local dependencies leaked through (fixed paths, machine-specific
  env vars, local databases, etc.)
- All functionality should work, except those explicitly gated behind
  permissions (e.g. specific API access)

> This step cannot be automated — it requires real human verification.

---

## Requirement 5 — Pack clean & publish (via skill-release-plus)

**Use [skill-release-plus](https://github.com/Songhonglei/build-better-skills/tree/main/skills/skill-release-plus) to sign, pack, and publish** to one or more skill hubs
(clawhub by default, or fan out to multiple via `--target`).

Mandatory checklist before executing:
- [ ] **Show the user a summary of changes + acceptance report + clickable
  preview URL, and wait for explicit acceptance** — don't self-test → upload →
  publish in one shot
- [ ] Confirm version policy (auto-bump / manually specified)
- [ ] Collect the changelog text
- [ ] Get an explicit "confirm publish" reply from the user

```
Invoke skill-release-plus → point it at your skill directory
```

**Before packing**, verify:
- [ ] No test scripts, temp files, or backup files in the skill directory
- [ ] All build artifacts live in `output/` (or elsewhere), not in the skill dir
- [ ] The `.skill` archive is built from the latest code, not an older snapshot

After publish, verify on the hub page that the skill name, description, and
version look correct.
