# Skill Launch Rubric

Use this rubric after running `scripts/audit_skill.py` or when judging a skill manually.

## Severity

- P0: Blocks launch. The skill is missing required files, has malformed frontmatter, or may expose secrets.
- P1: High-priority adoption or safety issue. Fix before publishing broadly.
- P2: Quality issue. Fix when it materially improves install confidence or agent reliability.
- P3: Polish. Fix opportunistically.

## Scoring

The audit score is intentionally adoption-weighted:

- Trigger quality: 30 points. `name` and `description` must make the skill discoverable and invokeable.
- Structure: 25 points. The body must teach a workflow and reference bundled files correctly.
- Compatibility: 15 points. The skill should run as a plain AgentSkill unless a runtime is essential.
- Safety: 15 points. Credentials, destructive commands, publishing, payments, and external messages need guardrails.
- Market readiness: 15 points. The first screen, output contract, and summary must make the value obvious.

## Strong Launch Checklist

- `SKILL.md` exists at the root.
- Frontmatter contains `name` and `description`.
- `name` is lowercase hyphen-case.
- `description` says what the skill does and when to use it.
- The body starts with quick usage or a workflow.
- Scripts are directly runnable and documented.
- References are linked from `SKILL.md` only when needed.
- No local absolute paths, private account names, real secrets, or machine-only assumptions.
- Sensitive operations use preview, dry-run, or explicit confirmation.
- The package has one canonical source of truth and avoids duplicate docs inside the skill.

## Launch Verdicts

- 90-100: Ready. Publish after one realistic forward test.
- 80-89: Ready with fixes. Publish after resolving P1 findings.
- 65-79: Needs work. The concept is probably valid, but agent execution or install confidence is weak.
- Below 65: Not ready. Rework trigger surface, structure, or safety before launch.
