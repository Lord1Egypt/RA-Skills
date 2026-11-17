## Description:

Release skills to ClawHub through a publication pipeline covering scaffolding, OPSEC scanning, review, staging, publishing, and security scan verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chunhualiao](https://clawhub.ai/user/chunhualiao)

### License/Terms of Use:

MIT

## Use Case:

Developers and release operators use this skill to prepare, validate, stage, review, publish, and verify agent skill releases on ClawHub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can exercise high-impact release authority over GitHub and ClawHub.

Mitigation: Use it only when the agent is meant to have release authority, narrow the trigger set, and require explicit confirmation before repo creation, first push, force push, visibility changes, and publish.

Risk: Security evidence reports weak gating and flawed validation checks.

Mitigation: Fix the validation scripts so checks fail closed and match the documented hard gates before relying on automated release decisions.

## Reference(s):

- [Skill Releaser on ClawHub](https://clawhub.ai/chunhualiao/skills/skill-releaser)
- [Release pipeline validation scripts](scripts/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, generated release files, configuration, and review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify skill release files and propose privileged GitHub and ClawHub commands when used with the required tools.]

## Skill Version(s):

1.5.0 (source: frontmatter, skill.yml, CHANGELOG, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
