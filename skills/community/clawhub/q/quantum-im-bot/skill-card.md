## Description:

量子密信即时通讯渠道插件，将 OpenClaw 接入量子密信平台，实现 AI 智能回复、多账号管理、安全配对，并支持文本、图片、文件、图文消息以及群聊和私聊。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mildniu](https://clawhub.ai/user/mildniu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to connect an OpenClaw agent to the Quantum IM messaging platform for direct and group chat replies, multi-account operation, and text or media message handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes an inbound webhook that can dispatch messages to an agent.

Mitigation: Protect the webhook with authentication or signatures, require HTTPS, and enforce pairing or allowlist checks before agent dispatch.

Risk: Credentials and message data may be sent through configurable HTTP endpoints or plaintext URL parameters.

Mitigation: Use HTTPS for inbound and outbound traffic and treat existing keys as sensitive secrets that should not be exposed in logs or URLs.

Risk: Media uploads can read local file paths and send files to the Quantum IM API.

Mitigation: Restrict media uploads to an approved directory or opaque media IDs and keep request size and rate limits in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mildniu/skills/quantum-im-bot)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [ClawHub plugin marketplace](https://clawhub.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and Quantum IM robot credentials; supports direct and group chats plus text, image, file, and news messages.]

## Skill Version(s):

1.0.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
