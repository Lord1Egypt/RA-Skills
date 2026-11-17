## Description:

Sends international SMS (USMS) via uspeedo platform HTTP API for single or batch verification, notification, and marketing messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[code-by-ai](https://clawhub.ai/user/code-by-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an agent through sending international SMS via uspeedo, including credential checks, template selection, recipient formatting, API calls, and result reporting. It is intended for verification, notification, marketing, and batch SMS workflows where the user has proper authorization and recipient consent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send SMS through the user's uspeedo account and may create cost, compliance, or unwanted-message exposure if recipients, message body, SMS type, or batch size are wrong.

Mitigation: Review the recipient list, message body, SMS type, expected cost, and legal consent before each send, especially for batch or marketing messages.

Risk: The skill requires uspeedo access keys, and exposing those keys in chat, logs, scripts, or shell history could allow unauthorized SMS sending.

Mitigation: Keep access keys in environment variables or a protected .env file, avoid hardcoding or pasting secrets into prompts, and rotate credentials if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/code-by-ai/skills/send-usms-uspeedo)
- [uspeedo homepage](https://uspeedo.com)
- [uspeedo SMS API documentation](https://docs.uspeedo.com/docs/sms/api/)
- [uspeedo AI communication console](https://uspeedo.com/en/ai-communication?SaleCode=JD4651&ChannelCode=OpenClaw)
- [uspeedo SMS template management](https://console.uspeedo.com/sms/template)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a uspeedo API request body, curl command, credential setup guidance, and success or error interpretation.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
