## Description:

Agent lifecycle hook system for OpenClaw that uses heartbeat polling and subagent patterns to simulate key lifecycle event triggers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sipoon](https://clawhub.ai/user/sipoon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to reason about OpenClaw lifecycle hooks, configure practical event-triggered behaviors, and understand which hook types require convention-based handling instead of kernel interception.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to create session-end cron tasks, run heartbeat-driven checks, spawn subagents, or write memory logs automatically.

Mitigation: Enable lifecycle hooks only after review, keep scheduling and memory-write scopes explicit, and provide a clear way to disable or audit the automation.

Risk: Tool-level pre-use and post-use hooks are described as convention-based rather than kernel-enforced.

Mitigation: Treat destructive-operation checks as agent behavior guidance that still requires user review and confirmation before risky actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sipoon/skills/sipoon-lifecycle-hooks)
- [Publisher profile](https://clawhub.ai/user/sipoon)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline code and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose lifecycle automation patterns, cron scheduling, subagent coordination, and memory-log writes for review before use.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter says 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
