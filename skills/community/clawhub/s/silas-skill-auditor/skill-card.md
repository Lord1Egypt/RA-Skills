## Description:

Audits installed or remote agent skills for code security, permission risks, data leakage, and content-compliance concerns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[langhuachuanshi](https://clawhub.ai/user/langhuachuanshi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to inspect skills before installation or after installation and produce a structured security review with findings, scoring, and recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect skill directories and surface sensitive-looking strings found during review.

Mitigation: Use it only for explicit skill-audit tasks and do not send discovered secrets or tokens to external services.

Risk: The documented pre-install review workflow uses a fixed /tmp/skill-audit-tmp path.

Mitigation: Use a uniquely generated private temporary directory and guarded cleanup before deleting review files.

Risk: Broad trigger wording can cause the skill to run outside a clear audit request.

Mitigation: Invoke it only when the user explicitly requests a skill audit, safety check, or security review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/langhuachuanshi/skills/silas-skill-auditor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown security review report with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes file inventory, categorized risk findings, instruction analysis, score, rating, and recommendations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
