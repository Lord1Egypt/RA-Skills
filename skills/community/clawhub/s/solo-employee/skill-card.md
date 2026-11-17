## Description:

Solo Employee guides an OpenClaw agent to act as an employee that receives CEO-assigned tasks, clarifies unclear requirements, produces structured deliverables, and handles follow-up refinement within a five-turn limit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moistenxx](https://clawhub.ai/user/moistenxx)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and agent builders use this skill to make an OpenClaw agent operate as a task-executing employee in a solo-company workflow coordinated by a CEO agent. It helps the agent parse assigned work, ask for clarification when needed, return structured Markdown deliverables, and report completion status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user could try to gain coordinator authority by prefixing a message with '[CEO]' or '【任务分配】'.

Mitigation: Keep platform, system, safety, and user-approval rules above the skill, and only treat CEO-style task prefixes as authoritative when the coordinator is already trusted.

Risk: The five-turn workflow limit can force a response before all ambiguity is resolved.

Mitigation: When the limit is reached or external dependencies block completion, report the current deliverable, unresolved assumptions, and remaining confirmation needs clearly.

## Reference(s):

- [Employee SOUL.md role template](references/employee_soul_template.md)
- [Solo Employee ClawHub release](https://clawhub.ai/moistenxx/skills/solo-employee)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown with structured status sections and optional fenced code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses follow employee-reporting templates, include completion status, and are limited to at most five interaction rounds with the CEO coordinator.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
