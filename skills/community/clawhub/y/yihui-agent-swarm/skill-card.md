## Description:

Multi-agent orchestration framework for OpenClaw that defines roles, routes tasks, manages state, and coordinates agent teams with structured YAML configuration and message protocols.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1yihui](https://clawhub.ai/user/1yihui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to design and run OpenClaw multi-agent teams with master, specialist, critic, and router roles. It helps structure task routing, review, state tracking, memory recall, and cross-agent handoffs for operational and research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad cross-agent memory recall and automatic persistence can expose sensitive conversations, operational data, user profile details, secrets, or incident records across users or roles.

Mitigation: Scope MemPalace and Cortex access by user, tenant, task, and agent role; require validation or explicit approval before writing preferences, profile data, secrets, incident details, or system-change records.

Risk: Unscoped agent handoffs and channel targets can route task context to the wrong agent or communication destination.

Mitigation: Review team YAML before deployment, require explicit per-agent targets, and test routing rules and escalation paths with non-sensitive data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1yihui/skills/yihui-agent-swarm)
- [Project source listed in skill metadata](https://github.com/1yihui/YiHui)

## Skill Output:

**Output Type(s):** [Markdown, Configuration, Guidance]

**Output Format:** [Markdown guidance with YAML configuration and workflow examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes role definitions, routing rules, memory protocols, structured message formats, and example workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
