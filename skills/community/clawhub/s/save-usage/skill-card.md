## Description:

Classifies tasks by safety and complexity to route safe, negligible queries to gpt-5.1-codex-mini and escalate critical, executable, uncertain, or high-impact tasks to gpt-5.3-codex.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jacks3tr](https://clawhub.ai/user/jacks3tr)

### License/Terms of Use:


## Use Case:

Developers and Codex users use this skill to decide when a task can stay on a smaller model for safe, low-impact work and when it should be escalated to a stronger Codex model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may forward the full task description into a spawned session, which can include secrets, proprietary code, personal data, or cost-sensitive work.

Mitigation: Review tasks before use in sensitive conversations and avoid invoking the skill where full-task forwarding is not acceptable.

Risk: The skill broadly escalates executable, uncertain, structured, or high-impact tasks, which may increase cost-sensitive model usage.

Mitigation: Use in contexts where the routing tradeoff is acceptable and review cost-sensitive workflows before installing.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/jacks3tr/skills/save-usage)
- [Publisher profile](https://clawhub.ai/user/jacks3tr)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with model-routing decisions and escalation criteria]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to spawn a stronger model session for executable, uncertain, structured, or high-impact tasks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
