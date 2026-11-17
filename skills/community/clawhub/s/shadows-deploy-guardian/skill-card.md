## Description:

Pre-deployment verification checklist - tests, types, build, secrets scan, environment validation. Use before pushing to production or staging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nakedoshadow](https://clawhub.ai/user/nakedoshadow)

### License/Terms of Use:

MIT

## Use Case:

Developers and release engineers use this skill before staging or production deployment to check repository status, tests, type and lint results, build readiness, secrets exposure, and environment setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run project-controlled test, lint, type-check, and build commands that may execute repository code.

Mitigation: Use it only on trusted repositories or in a sandboxed CI runner with minimal credentials.

Risk: Unpinned npx commands may execute unexpected tool versions or downloaded code.

Mitigation: Prefer local pinned tool dependencies or no-install execution before using the skill for production deployment review.

Risk: The secrets scan may print matched credential-like values into terminal output.

Mitigation: Run the scan in a private terminal or CI log context where output is not shared or retained broadly.

## Reference(s):

- [Shadows Deploy Guardian on ClawHub](https://clawhub.ai/nakedoshadow/skills/shadows-deploy-guardian)
- [nakedoshadow publisher profile](https://clawhub.ai/user/nakedoshadow)
- [ClawHub homepage metadata](https://clawhub.ai/NakedoShadow)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Analysis, Guidance]

**Output Format:** [Markdown report with gate results, blockers, warnings, and a recommended deployment command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report summarizes six deployment gates and returns PASS, FAIL, SKIP, WARN, CLEAR TO DEPLOY, BLOCKED, or CLEAR WITH WARNINGS statuses.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
