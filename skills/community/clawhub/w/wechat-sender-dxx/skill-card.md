## Description:

Helps an agent send WeChat text, image, and file messages through the OpenClaw Weixin channel to existing contacts or chats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntaffffff](https://clawhub.ai/user/ntaffffff)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to send WeChat notifications or one-off messages through a local OpenClaw Gateway when WeChat is configured and the recipient already has a chat history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messages may be sent without enforced user authorization in the packaged sender path.

Mitigation: Require explicit human approval or gateway-level authorization before each send, especially for group or bulk messages.

Risk: Recipient restrictions and contact allowlisting may not be enforced by the sender script.

Mitigation: Enforce a trusted recipient allowlist outside the script and send only to contacts or chats that have been pre-validated.

Risk: Rate limits are described but not meaningfully enforced in the actual send path.

Mitigation: Apply external quotas, cooldowns, and monitoring before enabling automated or repeated sends.

Risk: File sending may transmit local file contents before authorization, allowlisting, path review, and quota controls are fixed.

Mitigation: Avoid file sending until those controls are enforced in the actual send path.

## Reference(s):

- [WeChat Sender by dxx ClawHub page](https://clawhub.ai/ntaffffff/skills/wechat-sender-dxx)
- [WeChat API reference](references/wechat-api.md)
- [WeChat rate limits](references/rate-limits.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python, bash, and JSON snippets; sender scripts return JSON-like success or error status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local OpenClaw Gateway and configured openclaw-weixin channel.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
