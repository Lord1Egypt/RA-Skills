## Description:

Defines, enforces, and tracks structured workflows for any task type, including rules, execution sequences, hard gates, soft advisories, checkpoints, and violation detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyber-bye](https://clawhub.ai/user/cyber-bye)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to define repeatable task workflows and have an agent follow ordered steps, gates, checkpoints, rule checks, violation logging, and post-fix handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can influence agent-wide workflow behavior through global rules, hard gates, and checkpoint enforcement.

Mitigation: Review the global rules, gate conditions, and override policy before installation, and tailor them to the workspace owner's operating expectations.

Risk: The skill writes persistent workflow state, logs, statistics, and violation records that may include sensitive task details.

Mitigation: Use it only in workspaces where persistent audit records are acceptable, and review logging paths and retention practices before use.

## Reference(s):

- [Workflow Guardian Skill Page](https://clawhub.ai/cyber-bye/skills/workflow-guardian)
- [Publisher Profile](https://clawhub.ai/user/cyber-bye)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown instructions, workflow templates, rule files, logs, and JSON memory schema]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may write persistent workflow state, run logs, statistics, and violation records in the workspace.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
