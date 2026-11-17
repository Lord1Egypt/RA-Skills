## Description:

Configures and manages a QQ Official Bot with QQ platform setup, IP allowlist guidance, WebSocket connectivity, and OpenClaw AI integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byzgpc](https://clawhub.ai/user/byzgpc)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to deploy a QQ Official Bot that connects private, group, and channel messages to OpenClaw AI. It provides setup steps for QQ app credentials, IP allowlisting, bot runtime scripts, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A packaged credential-like QQ client secret could be copied into a deployment or reused accidentally.

Mitigation: Replace and rotate any QQ AppSecret that matches the packaged example, and keep bot secrets outside source-controlled files.

Risk: QQ messages, user identifiers, and replies may be written to local logs or queue files in plaintext.

Mitigation: Run the bot only where plaintext chat data is acceptable; use restrictive file permissions, log redaction or rotation, and explicit consent for private or group chat processing.

Risk: The skill runs networked bot code and installs unpinned Python dependencies.

Mitigation: Review the scripts before execution, pin and audit dependencies, and deploy from an isolated account or workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/byzgpc/skills/qqbot)
- [QQ Bot platform documentation](https://bot.q.qq.com/wiki)
- [QQ Bot API documentation](https://bot.q.qq.com/wiki/develop/api/)
- [QQ Bot gateway intents](https://bot.q.qq.com/wiki/develop/api/gateway/intents.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown documentation with inline JSON, Python, and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes runnable QQ bot and helper scripts; requires local credential and IP allowlist configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
