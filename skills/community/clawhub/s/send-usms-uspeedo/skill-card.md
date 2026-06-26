## Description: <br>
Sends international SMS (USMS) via uspeedo platform HTTP API for batch SMS, verification, notification, and marketing messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[code-by-ai](https://clawhub.ai/user/code-by-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure USpeedo credentials and send international SMS messages for verification, notifications, marketing, or batch communication workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SMS recipients and message content are shared with USpeedo using account credentials. <br>
Mitigation: Review recipients and message text before sending, and avoid sending secrets or regulated sensitive information by SMS. <br>
Risk: Incorrect or stale USpeedo credentials can cause failed sends or authentication errors. <br>
Mitigation: Store credentials in environment variables, rotate them when needed, and verify template IDs before approving a send. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/code-by-ai/send-usms-uspeedo) <br>
- [USpeedo homepage](https://uspeedo.com) <br>
- [USpeedo SMS API documentation](https://docs.uspeedo.com/docs/sms/api/) <br>
- [USpeedo AI communication portal](https://uspeedo.com/en/ai-communication?SaleCode=JD4651&ChannelCode=OpenClaw) <br>
- [USpeedo SMS template management](https://console.uspeedo.com/sms/template) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send phone numbers and SMS message content to USpeedo through the user's configured account credentials.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
