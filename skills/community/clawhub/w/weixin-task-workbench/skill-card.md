## Description:

Weixin Task Workbench lets an OpenClaw agent manage multiple ongoing WeChat tasks through one chat window, routing each task to an isolated session while maintaining task status, summaries, and archive state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawnhan98](https://clawhub.ai/user/shawnhan98)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to provide a single WeChat task workbench where users can create, switch, continue, summarize, close, and archive parallel tasks without mixing their contexts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registry restoration may silently copy task data and session keys across WeChat account boundaries.

Mitigation: Require the publisher to remove or clearly disclose cross-account restoration behavior and constrain registry operations to the active account/contact path before installation.

Risk: Task status diagnostics may expose session keys or raw registry paths.

Mitigation: Redact or gate sessionKey and raw path diagnostics so they are only shown when needed for authorized troubleshooting.

Risk: Session-tool access can affect task creation, routing, and history retrieval.

Mitigation: Pair session-tool allowlisting with strict ownership checks and narrow filesystem scope.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shawnhan98/skills/weixin-task-workbench)
- [Single-entry multi-task workbench protocol](references/protocol.md)
- [Weixin task workbench implementation notes](references/implementation.md)
- [Weixin Task Workbench test matrix](references/test-matrix.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown/text responses with inline shell commands and JSON task registry data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 plus session tools for task creation, routing, and history retrieval.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
