## Description:

PUA pushes an agent toward high-agency, exhaustive problem-solving when users express frustration, repeated failures, passive behavior, or quality complaints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanweai](https://clawhub.ai/user/tanweai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to make an agent persist through difficult tasks, verify claims with evidence, and escalate troubleshooting after repeated failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill broadly changes agent behavior and retry limits across all task types without clear safety boundaries.

Mitigation: Install it only when persistent escalation is desired, and set explicit stopping criteria, tool-use approval, and cost limits before use.

Risk: The security guidance classifies the release as suspicious because it is designed to make the agent persist harder and escalate after failures.

Mitigation: Supervise tool use and side effects during runs, especially on tasks that can spend money, modify files, call services, or affect external systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tanweai/skills/pua)
- [Full version referenced by artifact](https://github.com/tanweai/pua)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown or task-specific text with code and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable payload in the artifact; behavior may increase retry persistence and escalation across task types.]

## Skill Version(s):

2.9.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
