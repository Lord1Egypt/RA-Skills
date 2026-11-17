## Description:

Send text as voice messages across chat channels using text-to-speech, audio conversion, and platform-specific delivery guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xmanrui](https://clawhub.ai/user/xmanrui)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to generate Ogg/Opus voice files from text and send them as chat voice messages. It provides channel-specific guidance for Feishu/Lark, Discord, Telegram, Signal, WhatsApp, and similar platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chat credentials may be exposed if Feishu tenant tokens are passed on the command line.

Mitigation: Use environment variables or a secret manager for tokens and avoid logging commands that include credentials.

Risk: Private message text may be sent to text-to-speech or chat platform APIs.

Mitigation: Convert only content approved for those services and avoid sensitive text unless that disclosure is acceptable.

Risk: Voice messages may be sent to the wrong recipient or platform.

Mitigation: Verify the recipient identifier, receive_id_type, and channel before sending.

## Reference(s):

- [Voice Reference](references/voices.md)
- [Feishu Open API](https://open.feishu.cn/open-apis)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with command examples and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for generating voice files, Discord waveform metadata, and platform-specific send requests.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
