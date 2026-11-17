---
name: tap-skill-preflight
description: Validate a SKILL.md before publishing — checks frontmatter completeness, semver, and that every declared bin actually resolves on PATH. Use before `clawhub publish`, or when a skill fails to load / shows as missing requirements.
version: 1.0.0
metadata:
  openclaw:
    emoji: ✅
    requires:
      bins: [python3] # stdlib only, no pip deps
---

# Skill Preflight

A **deterministic, self-validating** skill: it runs a real check with `python3`
and returns an honest machine-readable outcome. `ok:true` proves the target
`SKILL.md` passed *every* check below — nothing more, nothing less.

This is the executable-validation pattern: encode the process, run it with a real
tool, and gate the result on a postcondition instead of trusting a vibe.

## Trigger

- `/skill-preflight <path-to-SKILL.md | skill-folder>`
- Natural language: "check my skill before publishing", "why is my skill missing
  requirements", "validate this SKILL.md".

## Execution

Run the bundled checker against the target skill:

```bash
python3 scripts/preflight.py <path-to-SKILL.md | skill-folder>
```

It emits JSON `{ ok, reason, checks[] }` and exits `0` on pass, `1` on fail,
`2` on usage/IO error.

## Checks (the validation gate)

1. **frontmatter-present** — a `--- … ---` YAML block exists.
2. **has-name / has-description / has-version** — required keys are present and
   non-empty.
3. **version-semver** — `version` matches `N.N.N`.
4. **requires.bins-declared** — `metadata.openclaw.requires.bins` is declared
   (an empty list is fine; *absent* is not).
5. **bin:<name>** — every declared binary actually resolves on `PATH`
   (`shutil.which`). This is the real-execution gate: a skill that declares a
   tool it can't find will show as "missing requirements" at load time.

## Honest outcome contract

- `ok:true` → the SKILL.md passed all checks above. It does **not** guarantee the
  skill's behaviour is correct, only that its manifest is loadable and its
  declared tools are present.
- `ok:false` → `reason` names the failing checks; `checks[]` gives per-check
  detail. Fix those before `clawhub publish`.

## Examples

```
$ python3 scripts/preflight.py ./my-skill/SKILL.md
{ "ok": true, "reason": "all checks passed", "checks": [ ... ] }

$ python3 scripts/preflight.py ./broken/SKILL.md
{ "ok": false, "reason": "failed: version-semver, bin:jq", "checks": [ ... ] }
```

## Notes

- Pure Python standard library — no `pip install`, no network.
- Parses frontmatter without PyYAML so it runs anywhere `python3` exists.
