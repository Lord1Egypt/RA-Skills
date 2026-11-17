## Description:

Send Feishu or Lark webhook messages as plain text, rich text posts, or interactive cards, with optional image upload using a tenant access token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianheihei002](https://clawhub.ai/user/tianheihei002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to prepare and send Feishu or Lark group webhook notifications, including formatted posts, interactive cards, and uploaded image assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send user-selected content to external Feishu or Lark destinations.

Mitigation: Verify the webhook URL and exact message content before sending.

Risk: Tenant access tokens may be exposed if passed on the command line.

Mitigation: Store FEISHU_TENANT_ACCESS_TOKEN in a protected secret store or environment variable and avoid the documented --token argument.

Risk: Uploaded images or message content may contain sensitive data.

Mitigation: Upload images and send content only when they are intended to be shared in the target Feishu or Lark destination.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tianheihei002/skills/yq-feishu-webhook-skill)
- [Feishu Open Platform](https://open.feishu.cn)
- [Feishu image upload API](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/image/create)
- [Feishu file upload API](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/file/create)
- [Feishu user identity documentation](https://open.feishu.cn/document/home/user-identity-introduction/open-id)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Feishu/Lark message JSON, webhook request guidance, and image upload command examples.]

## Skill Version(s):

1.0.0 (source: frontmatter, artifact metadata, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
