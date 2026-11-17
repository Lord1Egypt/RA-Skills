## Description:

Coordinate agents toward a unified objective; assign roles, sequence work, prevent conflicts, and define success criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzfshark](https://clawhub.ai/user/mzfshark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent coordinators use this skill to turn a shared objective and current system state into a structured multi-agent execution plan with owners, handoffs, dependencies, validation checkpoints, and success criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases may activate this planning skill for ordinary coordination requests.

Mitigation: Review the generated plan before acting on it and confirm it applies to the current objective.

Risk: An orchestration plan may include irreversible or high-impact actions as proposed next steps.

Mitigation: Require explicit approval and governance alignment before carrying out irreversible actions.

Risk: Unclear delegation boundaries can move judgment or risk evaluation to the wrong agent.

Mitigation: Keep strategic judgment and risk evaluation with the responsible owner, and delegate only bounded execution tasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mzfshark/skills/strategic-orchestration)
- [ClawHub publisher profile](https://clawhub.ai/user/mzfshark)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown guidance with ordered steps, role assignments, dependencies, handoff messages, and success criteria.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires objective and system_state inputs; the skill itself does not request tool execution or external credentials.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact metadata reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
