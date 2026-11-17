## Description:

Sends inline images to Feishu chats by uploading through the Feishu Open API and sending an image message with the resulting image_key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jamesqin-cn](https://clawhub.ai/user/jamesqin-cn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to send images that render inline in Feishu chat when standard message-file delivery does not render images correctly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill evidence reports exposed and mishandled Feishu credentials.

Mitigation: Review before installation, rotate any real exposed Feishu app secret, and remove hardcoded credentials before use.

Risk: Direct API sending can act under a Feishu app identity without the usual message-tool path.

Mitigation: Require explicit user or administrator approval and use a narrowly scoped Feishu app identity.

Risk: Temporary scripts can contain credentials while image sending is performed.

Mitigation: Avoid writing secrets into temporary scripts, or delete temporary scripts immediately after execution and restrict file access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jamesqin-cn/skills/send-feishu-image)
- [Feishu Upload Image API](https://open.feishu.cn/document/ukTMukTMukTM/ukTM5UjL5ETO14COxkTN/1images-1upload)
- [Feishu Send Message API](https://open.feishu.cn/document/ukTMukTMukTM/ukTM5UjL5ETO14COxkTN/1messages-1create)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a temporary Node.js workflow for Feishu image upload and message sending.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
