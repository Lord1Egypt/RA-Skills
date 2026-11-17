## Description:

SafeProactive is a local safety framework for autonomous agents that uses Write-Ahead Logging and mandatory human approval gates to preserve auditability and oversight.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rigeneproject](https://clawhub.ai/user/rigeneproject)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use SafeProactive to configure autonomous agents so intended actions are proposed, logged locally, checked against safety constraints, and routed to human approval for higher-risk capability expansion or protocol changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Global agent governance may affect every turn and broaden the skill's influence beyond a narrow task.

Mitigation: Narrow activation away from every_turn and enable the skill only in workspaces where this safety posture is intended.

Risk: Unrestricted system prompt prepending can make the framework difficult to bypass when a task needs a different operating mode.

Mitigation: Avoid unrestricted prompt prepending and document when the SafeProactive instructions are active.

Risk: Recurring autonomous logging or actions can exceed the declared local scope if workspace, memory, network, and notification behavior are not aligned.

Mitigation: Require approval for first-contact external APIs and physical actions, define log redaction rules, and align declared permissions with actual behavior.

## Reference(s):

- [SafeProactive ClawHub page](https://clawhub.ai/rigeneproject/skills/safeproactive)
- [README](artifact/README.md)
- [SKILL](artifact/SKILL.md)
- [CLAW_HUB_METADATA](artifact/CLAW_HUB_METADATA.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline YAML and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts agent behavior around local WAL, approval gates, and security posture; does not itself execute actions.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
