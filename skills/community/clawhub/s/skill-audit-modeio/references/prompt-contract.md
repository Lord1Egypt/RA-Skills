# Skill Safety Assessment contract (`static_repo_scan`)

Use this contract when the user asks for a deterministic pre-install repository audit of a skill, plugin, or extension repository.

## Script-first workflow

```bash
python3 scripts/skill_safety_assessment.py evaluate --target-repo <repo_path> --json > /tmp/skill_scan.json
python3 scripts/skill_safety_assessment.py prompt --target-repo <repo_path> --scan-file /tmp/skill_scan.json --include-full-findings
python3 scripts/skill_safety_assessment.py validate --scan-file /tmp/skill_scan.json --assessment-file /tmp/assessment.md --json
python3 scripts/skill_safety_assessment.py adjudicate --scan-file /tmp/skill_scan.json --assessment-file /tmp/adjudication.json --json
```

Compatibility alias:

```bash
python3 scripts/skill_safety_assessment.py scan --target-repo <repo_path> --json > /tmp/skill_scan.json
```

## Hard constraints

1. Static analysis only. Do not execute code, install dependencies, or run hooks.
2. Every finding must include file, line, exact snippet, and evidence refs.
3. `script_scan_json` is the authoritative baseline. Do not ignore required highlight evidence IDs.
4. If visibility is incomplete, return `caution` and explain coverage limits.
5. Treat docs/examples/tests carefully; do not imply runtime exploitability without supporting evidence.

## Required output sections

- Decision card with `reject`, `caution`, or `approve`
- Risk score and confidence
- Evidence-backed top findings
- Likely exploit chain
- Safe-to-run subset
- Priority-ordered remediation plan
- `# JSON_SUMMARY` machine-readable block

## Reviewer checklist

- All findings have concrete evidence.
- All findings include `evidence_refs`.
- Required highlight IDs are covered.
- No execution steps were performed.
