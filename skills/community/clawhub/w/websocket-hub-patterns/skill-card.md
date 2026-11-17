## Description:

Horizontally-scalable WebSocket hub pattern with lazy Redis subscriptions, connection registry, and graceful shutdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to design horizontally scalable real-time WebSocket services with Redis-backed coordination for chat, collaborative editing, and live dashboard workloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install instructions rely on mutable external commands or references that can change over time.

Mitigation: Review installer content before execution and prefer pinned, reviewed installer versions or immutable source references.

Risk: WebSocket and Redis deployments can expose sensitive message contents or overly broad channel access if data handling is not reviewed.

Mitigation: Review Redis data contents, channel naming, retention, and access controls before adopting the pattern.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wpank/skills/websocket-hub-patterns)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Go code snippets and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes implementation patterns, decision guidance, and anti-patterns for Redis-backed WebSocket hubs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
