---
name: skill-checker
description: Audit a target SKILL.md against the Agent Skills specification and generate a Chinese HTML report. Use when the user asks to check, audit, review, or optimize a SKILL.md file, verify whether a skill file follows specification rules, identify severe or warning issues, or produce a shareable compliance report for a SKILL.md path or a skill directory path.
license: MIT
metadata:
  author: oahcfly
  version: 1.0.2
---

# Skill Checker

Check only `SKILL.md`.

Use this skill when the user explicitly wants to check, audit, review, or optimize a `SKILL.md` file.

Accept either a `SKILL.md` path or a skill directory path. If the input is a directory, resolve `SKILL.md` inside it before running any checks.
Support absolute paths directly. Prefer absolute paths when auditing skills outside the current workspace.

Run the checker script (PowerShell):

```powershell
# Auto locate this skill directory (works even if you run from another folder)
$SkillDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $SkillDir

# Run
python .\scripts\check_skill.py <target-path> [--out <report-path>]
```

Use `--fail-on-audit` only when a strict CI-style exit code is required.

Example with absolute paths:

```powershell
$SkillDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $SkillDir
python .\scripts\check_skill.py "C:\path\to\skill\SKILL.md" --out ".\reports\skill-report.html"
```

Strict exit code example:

```powershell
python .\scripts\check_skill.py "C:\path\to\skill\SKILL.md" --out ".\reports\skill-report.html" --fail-on-audit
```

Use the generated HTML report as the primary output. Summarize the overall result, the severe issue count, and the highest-priority fixes in the final response.

## What to check

Validate the target `SKILL.md` against the Agent Skills specification:

1. Confirm YAML frontmatter exists and is parseable.
2. Confirm required fields such as `name` and `description`.
3. Validate optional specification fields when present.
4. Check that `name` matches the skill directory name when it can be inferred.
5. Review whether `description` says what the skill does and when to use it.
6. Review whether the body contains enough actionable guidance to help another agent execute the skill.

Treat specification violations as severe issues.

Treat obvious semantic failures as severe issues too, including:

- descriptions that are too short or too vague to support triggering
- bodies that are nearly empty or do not provide actionable guidance

Treat weaker organization or thin guidance as warnings.

Return a failing result when severe issues are `2` or more. Otherwise return a passing result.

## Reporting

Always point the user to the generated HTML report path, especially when the target skill lives outside the current repo.

When summarizing results:

1. State whether the result is passing or failing.
2. Mention the severe issue count and warning count.
3. Call out the first fixes the user should make.

## References

Read `references/specification-checklist.md` when you need the exact rules and severity mapping used by this skill.
