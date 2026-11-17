## Description:

尸狗·警觉魄v2.0 helps an agent produce security assessments, threat intelligence checks, monitoring summaries, hardening recommendations, and incident response guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lt8899789](https://clawhub.ai/user/lt8899789)

### License/Terms of Use:

MIT-0

## Use Case:

Security engineers, developers, and operators use this skill to ask an agent for security audits, threat detection analysis, compliance checks, attack-surface assessment, and incident response recommendations. Keep it report-only unless the deployment explicitly approves monitoring or response actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to monitor and respond broadly without clear approval, scope, or rollback safeguards.

Mitigation: Keep the skill report-only by default; before enabling monitoring or response actions, define systems, files, accounts, duration, and tools in scope.

Risk: Response actions such as blocking activity, locking accounts, quarantining or removing files, or applying repairs could disrupt systems if performed without approval.

Mitigation: Require separate human confirmation before any blocking, account lockout, quarantine, removal, or repair action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lt8899789/skills/shi-gou-guardian)
- [Publisher profile](https://clawhub.ai/user/lt8899789)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance, Configuration]

**Output Format:** [Markdown security reports with tables, findings, monitoring status, and prioritized recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report-only by default; response actions should require explicit scope and confirmation.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
