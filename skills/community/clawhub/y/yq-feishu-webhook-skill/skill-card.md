## Description: <br>
Sends Feishu/Lark webhook messages as plain text, rich text, or interactive cards, with optional image upload using a tenant access token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianheihei002](https://clawhub.ai/user/tianheihei002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to prepare and send Feishu/Lark group notifications, including formatted post messages, interactive cards, and image-backed messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send outbound Feishu/Lark messages or upload images to an external service. <br>
Mitigation: Use narrowly scoped webhook URLs and tenant tokens, keep secrets in environment variables, and require explicit user confirmation before sending messages or uploading images. <br>
Risk: Broad trigger wording could cause unintended message preparation or delivery. <br>
Mitigation: Confirm the target webhook, message type, recipients or mentions, and final content before any send action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tianheihei002/yq-feishu-webhook-skill) <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>
- [Feishu image upload API](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/image/create) <br>
- [Feishu file upload API](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/file/create) <br>
- [Feishu user identity guide](https://open.feishu.cn/document/home/user-identity-introduction/open-id) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON message bodies and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call Feishu/Lark webhook and image upload APIs when the user supplies a webhook URL and required credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, release evidence, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
