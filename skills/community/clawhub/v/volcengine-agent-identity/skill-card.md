## Description:

Provides OpenClaw agent identity workflows for UserPool login, TIP tokens, credential hosting, environment bindings, plugin configuration, and tool risk approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loveyana](https://clawhub.ai/user/loveyana)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to manage OpenClaw identity sessions, credential access, environment bindings, and risk approval flows for tools that need authenticated access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can participate in credential hosting, credential return, and environment variable binding workflows.

Mitigation: Install only where agent identity and credential management are intended, avoid returnValue unless needed, and review identity backend and environment binding policy before use.

Risk: High-risk tool approval affects whether sensitive or destructive tool calls can proceed.

Mitigation: Keep approval paths under human control and review risk classifications before approving blocked tool calls.

## Reference(s):

- [Volcengine Agent Identity skill page](https://clawhub.ai/loveyana/skills/volcengine-agent-identity)
- [Volcengine intelligent agent identity and permission management documentation](https://www.volcengine.com/docs/86848)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON-like tool results with configuration snippets and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return authentication URLs, redacted status summaries, credential metadata, risk classifications, and OpenClaw configuration fragments.]

## Skill Version(s):

0.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
