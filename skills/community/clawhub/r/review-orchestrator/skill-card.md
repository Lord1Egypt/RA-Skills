## Description:

Get multiple perspectives on your work \u2014 coordinate reviews across cognitive modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leegitw](https://clawhub.ai/user/leegitw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to select a review approach, run multi-perspective or cognitive reviews, and gate staged work with configurable quality checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The quality-gate feature can run a test command from workspace configuration.

Mitigation: Review .openclaw/review-orchestrator.yaml and .claude/review-orchestrator.yaml before using /ro gate, especially in untrusted repositories.

Risk: Review outputs may capture sensitive implementation details from the target workspace.

Mitigation: Inspect generated files under docs/reviews/ before sharing them outside the workspace.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leegitw/skills/review-orchestrator)
- [Publisher Profile](https://clawhub.ai/user/leegitw)
- [OpenClaw Configuration](.openclaw/review-orchestrator.yaml)
- [Claude Configuration](.claude/review-orchestrator.yaml)
- [Review Output Workspace](docs/reviews/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports and structured review or quality-gate summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write review findings and gate results under docs/reviews/.]

## Skill Version(s):

1.5.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
