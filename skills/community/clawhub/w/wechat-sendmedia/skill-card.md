## Description:

Wechat Sendmedia helps an agent send local images, screenshots, and other files to a WeChat conversation through OpenClaw by returning a plain-text media directive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[torry21th](https://clawhub.ai/user/torry21th)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when an OpenClaw WeChat agent needs to send an existing local image, screenshot, or document back to the current chat or an explicitly named recipient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A chat request could cause the agent to send an arbitrary readable local file path.

Mitigation: Restrict eligible media to a known workspace or upload directory and require confirmation before sending pre-existing local files.

Risk: Failure diagnostics can reveal local paths or account-token related details to chat participants.

Mitigation: Redact sensitive diagnostics before returning them and avoid exposing account-token path information in chat.

## Reference(s):

- [OpenClaw Weixin notes](references/openclaw-weixin-notes.md)
- [ClawHub skill page](https://clawhub.ai/torry21th/skills/wechat-sendmedia)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text or Markdown with MEDIA:file URI directives and concise diagnostics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include absolute local file paths and short troubleshooting fields when a send fails.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
