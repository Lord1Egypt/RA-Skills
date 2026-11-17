## Description:

SentiClaw provides Python middleware for OpenClaw agents that checks inbound and outbound text for prompt-injection patterns, identity spoofing claims, PII or secret leakage, rate and loop issues, and selected access risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[supertechgod](https://clawhub.ai/user/supertechgod)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use SentiClaw to add lightweight runtime checks, redaction, audit logging, and alert hooks around OpenClaw agent message handling. It is intended as AI-layer middleware, not as a replacement for sandboxing, tool authorization, network controls, or other execution-boundary protections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may over-rely on this package as a complete agent security boundary.

Mitigation: Use it only as lightweight text filtering and audit support unless additional enforcement exists at the tool, network, sandbox, and authorization boundaries.

Risk: Security evidence says the package overstates protections and has flawed or missing enforcement.

Mitigation: Review the behavior carefully before installing it as a security control, and validate critical protections with tests in the target agent environment.

Risk: SQLite audit logging may retain message metadata and security event details locally.

Mitigation: Set an explicit audit retention policy, choose an acceptable audit database path, and disable audit logging when local retention is not appropriate.

Risk: Alert integration can send security event metadata through external messaging channels.

Mitigation: Configure alert destinations deliberately and confirm that the selected Discord, Telegram, Slack, WhatsApp, or OpenClaw channel is approved for the data being sent.

Risk: Outbound filtering and access checks are helper-layer controls and may not cover all secrets, URLs, paths, or tool execution paths.

Mitigation: Keep independent secret scanning, allowlists, SSRF protections, spend controls, and tool authorization in the actual execution path.

## Reference(s):

- [SentiClaw on ClawHub](https://clawhub.ai/supertechgod/skills/senticlaw)
- [supertechgod Publisher Profile](https://clawhub.ai/user/supertechgod)
- [PHRAIMWORK LLC](https://phraimwork.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include configuration examples for owner IDs, trusted senders, redaction settings, audit logging, rate limits, and alert routing.]

## Skill Version(s):

1.0.0 (source: server release metadata, openclaw metadata, pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
