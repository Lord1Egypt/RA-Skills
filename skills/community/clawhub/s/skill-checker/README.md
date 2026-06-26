# Skill Checker

`skill-checker` is a reusable skill for checking whether a target `SKILL.md` follows the Agent Skills specification and for generating a static HTML report.

- Author: `oahcfly`
- Version: `1.0.2`
- License: `MIT`

## When to use

Use this skill when the user asks an agent to:

- check a `SKILL.md`
- audit a `SKILL.md`
- review whether a skill file follows the specification
- optimize a `SKILL.md` based on audit findings

## What it checks

The checker focuses on `SKILL.md` only.

- YAML frontmatter presence and parseability
- required fields such as `name` and `description`
- optional specification fields when present
- consistency between `name` and the skill directory name
- whether `description` explains what the skill does and when to use it
- whether the body provides enough actionable guidance

The final result is:

- `pass` when severe findings are fewer than `2`
- `fail` when severe findings are `2` or more

## Usage

Run the checker with either a `SKILL.md` absolute path or a skill directory absolute path.
Use placeholder paths in documentation so the examples stay portable across machines and repositories.
Recommended workflow: auto-locate the `skill-checker` directory, `cd` into it, then run via relative path.

```powershell
# Auto locate this skill directory (works even if you run from another folder)
$SkillDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $SkillDir

# Run
python .\scripts\check_skill.py "C:\path\to\skill\SKILL.md" --out ".\reports\skill-report.html"
```

You can also point it at a skill directory:

```powershell
$SkillDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $SkillDir
python .\scripts\check_skill.py "C:\path\to\skill" --out ".\reports\skill-report.html"
```

For CI or strict pipelines, add:

```powershell
python .\scripts\check_skill.py "C:\path\to\skill\SKILL.md" --out ".\reports\skill-report.html" --fail-on-audit
```

## Output

The script prints:

- final status
- severe finding count
- warning count
- generated HTML report path

Exit code behavior:

- Default: exit code `0` when the command itself runs successfully, even if audit result is fail.
- With `--fail-on-audit`: exit code `1` when severe findings are `2` or more.

Generated reports under `reports/` are ignored by Git.

## Project layout

```text
skill-checker/
  SKILL.md
  README.md
  .gitignore
  agents/openai.yaml
  scripts/check_skill.py
  references/specification-checklist.md
  tests/
```

## Tests

```powershell
python -m unittest discover -s .\tests -p "test_*.py"
```

## Notes

- This skill intentionally keeps its current `metadata` rule strict.
- HTML reports are meant for review and sharing; they are not committed by default.
