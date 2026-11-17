## Description:

Spawn isolated subagents to handle long-running, complex, or blocking tasks without stalling the main session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netanel-abergel](https://clawhub.ai/user/netanel-abergel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to decide when to delegate long-running, multi-step, blocking, or parallelizable work to a subagent and how to describe the delegated task clearly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delegated tasks involving email, calendar, or sending examples may expose or reuse sensitive information.

Mitigation: Confirm account authorization, limit retrieved data, avoid unnecessary retention, and review sensitive summaries before they are sent or reused.

Risk: Long-running or vague delegated tasks can fail, time out, or produce unusable results.

Mitigation: Use explicit task descriptions with inputs, outputs, completion criteria, and timeouts; retry with a simpler task or fall back to the main session after failure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/netanel-abergel/skills/spawn-subagent)
- [ClawHub publisher profile](https://clawhub.ai/user/netanel-abergel)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides task-description patterns, timeout guidance, completion handling, failure handling, and cost guidance for subagent delegation.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
