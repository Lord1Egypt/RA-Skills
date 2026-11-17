## Description:

Send one or many emails through Sendmux using approved mailbox or agent credentials, idempotency keys, attachments, MCP, CLI, SDKs, or HTTP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sendmux.ai](https://clawhub.ai/user/sendmux.ai)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to prepare or send individual and batch emails through Sendmux, including messages with attachments, after confirming the full message details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outbound messages could reach an unintended recipient or disclose sensitive content or attachments.

Mitigation: Review and confirm the sender, every recipient, subject, body, and attachment before each send or batch.

Risk: Sendmux credentials could be exposed or grant broader sending access than needed.

Mitigation: Use scoped credentials and keep secrets out of chat.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sendmux.ai/skills/sendmux-send-email)
- [Sendmux skills homepage (declared in skill metadata)](https://github.com/Sendmux/skills)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code]

**Output Format:** [Markdown with JSON, shell, HTTP, and TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sending requires confirmed message details and appropriate Sendmux authorization.]

## Skill Version(s):

1.0.11 (source: ClawHub release metadata; skill frontmatter: 1.7.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
