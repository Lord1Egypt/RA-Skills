## Description:

Records analytics issues and learnings in workspace Markdown logs to improve data quality, metrics, dashboards, and pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jose-compu](https://clawhub.ai/user/jose-compu)

### License/Terms of Use:

MIT-0

## Use Case:

Analytics developers and teams use this skill to record data quality incidents, metric drift, pipeline failures, dashboard problems, and feature requests for later review and improvement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning logs could retain sensitive analytics details.

Mitigation: Keep logs project-local and omit credentials, personal information, and raw query results.

Risk: Optional hooks may persist and inspect command output if enabled.

Mitigation: Review workspace-local hook configuration before enabling it; leave PostToolUse disabled unless output-based reminders are needed.

Risk: Promoting log entries into agent instructions or new skills could introduce inaccurate guidance.

Mitigation: Review the diff before promoting entries into AGENTS.md, MEMORY.md, hooks, or new skills.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/jose-compu/skills/self-improving-analytics)
- [Examples](artifact/references/examples.md)
- [OpenClaw integration](artifact/references/openclaw-integration.md)
- [Hook setup](artifact/references/hooks-setup.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands]

**Output Format:** [Markdown learning logs and setup guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persistent project-local learning logs; optional workspace-local reminders.]

## Skill Version(s):

1.1.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
