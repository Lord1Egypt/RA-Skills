## Description:

Captures learnings, errors, feature requests, corrections, knowledge gaps, and recurring best practices in Markdown so agents can promote durable improvements into project memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[f1zzyw](https://clawhub.ai/user/f1zzyw)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to record corrections, command failures, feature requests, knowledge gaps, and reusable practices as Markdown learning logs. They can then review those logs and promote durable lessons into project or workspace memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning logs can capture sensitive conversation details, command errors, private project context, or secrets.

Mitigation: Review entries before retention, redact secrets and private context, and prefer project-scoped .learnings files.

Risk: Optional hooks and promotion workflows can carry unreviewed or incorrect learnings into future agent instructions.

Mitigation: Require manual review before enabling hooks or promoting entries, avoid automatic promotion into instruction files, and verify hook scripts from the installed package.

Risk: Incorrect or stale learnings may persist and influence future agent behavior.

Mitigation: Keep entries status-tracked, resolve or retire outdated notes, and review promoted guidance before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/f1zzyw/skills/s1kasl-askdjna)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent learning, error, and feature-request entries for agent workflows.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
