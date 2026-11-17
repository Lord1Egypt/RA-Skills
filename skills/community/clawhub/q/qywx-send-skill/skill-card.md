## Description:

Sends Enterprise WeChat webhook messages in text, Markdown, Markdown V2, image, and news formats, with automatic chunking for long text-like messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wxf8126275](https://clawhub.ai/user/wxf8126275)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to send operational notifications, status updates, deployment notices, meeting reminders, images, and linked news-style messages to Enterprise WeChat group robots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messages and image data can be sent to a user-specified Enterprise WeChat webhook destination.

Mitigation: Use only approved webhook URLs, preferably enforced through an allowlist or managed configuration.

Risk: Image messages may read local file paths or fetch remote URLs before sending the resulting content.

Mitigation: Do not pass untrusted paths or URLs; add file type and size checks plus SSRF protections before deployment.

Risk: Sensitive operational data, secrets, or private images could be forwarded to chat recipients.

Mitigation: Review message content before sending and prohibit secrets or private operational data in webhook payloads.

Risk: Text messages include @all mention fields by default.

Mitigation: Require explicit confirmation or policy approval before sending @all messages.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wxf8126275/skills/qywx-send-skill)
- [Enterprise WeChat Developer Documentation](https://developer.work.weixin.qq.com/document/path/99110)
- [Webhook Send Message API](https://developer.work.weixin.qq.com/document/path/90236)
- [Enterprise WeChat Message Types](https://developer.work.weixin.qq.com/document/path/90237)
- [API Documentation](artifact/references/api_documentation.md)
- [Usage Examples](artifact/references/usage_examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text, Markdown, JSON webhook payloads, Python calls, and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May split long text, markdown, and markdown_v2 messages into multiple webhook sends; image messages are converted to base64 with an MD5 digest before sending.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
