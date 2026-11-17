## Description:

Work2cli Hitl with larkcli guides agents to turn recurring web-based work into local CLI tools, classify read versus write operations, and route write actions through a Feishu/Lark human-approval guard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[buger-gif](https://clawhub.ai/user/buger-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to convert repetitive work in web systems into reusable local CLI workflows. It is especially suited for agents that need to inspect system behavior, build read and write commands, document usage, and require human approval before changing remote state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may encourage broad reuse of browser sessions, copied request headers, or local token sources when building CLIs for arbitrary systems.

Mitigation: Use it only for systems where this behavior is explicitly authorized, prefer documented APIs and scoped credentials, and avoid copying full browser cookies, tokens, or headers unless there is a clear approved reason.

Risk: The Feishu/Lark approval guard is a soft control and can be bypassed by an actor that changes local code, configuration, credentials, or direct API calls.

Mitigation: Treat the guard as an anti-mistake review step, not a security boundary; use server-side approval, RBAC, short-lived credentials, and credential separation when hard enforcement is required.

Risk: Persistent local CLI tooling and a long-lived approval daemon can continue operating beyond the immediate task if deployed without review.

Mitigation: Review generated CLIs and daemon configuration before installation, keep audit logging enabled, limit approval daemon scope, and remove or disable unused integrations.

Risk: Incorrect read/write classification could let a state-changing operation bypass human approval.

Mitigation: Classify uncertain endpoints as write operations, require dry-run support for write commands, and have a human review the discovery report before implementation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/buger-gif/skills/work2cli-hitl)
- [Server-resolved source repository](https://github.com/buger-gif/work2cli-hitl)
- [Autonomous discovery guide](artifact/references/autonomous-discovery.md)
- [CLI design guide](artifact/references/cli-design-guide.md)
- [Write-guard HITL design](artifact/references/write-guard-hitl.md)
- [Self-evolution protocol](artifact/references/self-evolution.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples, implementation notes, and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing workflow guidance and CLI scaffolding patterns rather than a single executable artifact.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
