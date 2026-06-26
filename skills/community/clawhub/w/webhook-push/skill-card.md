## Description: <br>
Sends group bot messages to WeChat Work, DingTalk, and Feishu webhooks when an agent needs to push a notification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ysjyga](https://clawhub.ai/user/ysjyga) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent send prepared notifications to configured enterprise chat groups. It is suited to webhook-based messages, mentions, images, and markdown where the user has already supplied the platform key locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Webhook keys in webhook-config.json can authorize message delivery to enterprise chat groups if exposed or misused. <br>
Mitigation: Keep webhook-config.json private, avoid committing it, and use limited-purpose bot keys where the chat platform supports them. <br>
Risk: Messages, @mentions, or image paths may reach a broad or sensitive audience. <br>
Mitigation: Review the target platform, group, message content, mentions, and image path before allowing a send. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ysjyga/webhook-push) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples and optional shell command invocation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runtime behavior sends outbound webhook API requests using locally stored webhook keys.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
