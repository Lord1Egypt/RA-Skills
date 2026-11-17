## Description:

Route user tasks to the most relevant skills using a layered taxonomy, risk model, and minimum-necessary-loading strategy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wzk332266](https://clawhub.ai/user/wzk332266)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agent operators, and skill maintainers use this skill to choose relevant skills, classify newly installed skills, and maintain routing policy with risk and context-cost awareness. It is most useful in workspaces with many skills where routing decisions, overlap checks, and backlog review need consistent governance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can keep persistent local history of routing choices and task metadata.

Mitigation: Review what task details are logged before use, avoid sensitive prompt content in routing reasons, and disable or prune local routing logs when retention is not acceptable.

Risk: Helper scripts can download skills into a local inbox.

Mitigation: Review or disable intake automation before using the skill with untrusted skills, and keep newly downloaded skills blocked from risky actions until they are classified and approved.

Risk: A cleanup helper can delete a hard-coded inbox folder after confirmation.

Mitigation: Confirm the target inbox path before running cleanup and only run deletion after the skill import batch has been reviewed and preserved where needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wzk332266/skills/skill-taxonomy-router-pro)
- [Session Layer](references/session-layer.md)
- [Skill Classification Schema](references/skill-classification-schema.md)
- [Skill Index](references/skill-index.md)
- [Backlog Priority Report](references/backlog-priority.md)
- [New Skill Review](references/new-skill-review.md)
- [Risk Source Review](references/risk-source-review.md)
- [Skill Overlap Report](references/skill-overlap-report.md)
- [Skill Fusion View](references/skill-fusion-view.md)
- [Change Log](references/change-log.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, JSON, Files]

**Output Format:** [Markdown guidance with command examples and structured JSON or local file updates from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local skill indexes, usage counters, routing-decision logs, backlog reports, overlap reports, and intake state files.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
