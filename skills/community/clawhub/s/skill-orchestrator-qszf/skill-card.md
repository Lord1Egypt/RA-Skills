## Description:

Skill Orchestrator coordinates organization-wide skill optimization, task routing, inventory management, health monitoring, audit logging, and publishing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dxy0905](https://clawhub.ai/user/dxy0905)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, developers, and skill maintainers use this skill to route tasks to appropriate skills, coordinate multi-skill workflows, monitor skill health, and manage skill release operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes guidance for bypassing GitHub token redaction.

Mitigation: Remove token redaction bypass guidance and use approved authentication such as GitHub CLI, scoped short-lived tokens, or a secret store.

Risk: Persistent startup auto-load and automatic skill optimization or rollback can change agent behavior without explicit user intent.

Mitigation: Require explicit user confirmation before enabling startup auto-load, automated optimization, or rollback actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dxy0905/skills/skill-orchestrator-qszf)
- [ClawHub publisher profile](https://clawhub.ai/user/dxy0905)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with tables, workflow steps, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose skill routing, orchestration, health-check, audit, and configuration actions for human review.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
