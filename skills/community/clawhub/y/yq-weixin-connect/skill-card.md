## Description:

Guides an agent through binding a personal WeChat account to OpenClaw by installing the WeChat extension, generating a QR code, polling login status, storing credentials, and restarting the gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianheihei002](https://clawhub.ai/user/tianheihei002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect a personal WeChat account to an OpenClaw gateway through a QR-code login flow. It is not intended for WeCom or enterprise WeChat connections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may replace an existing OpenClaw WeChat extension and run npm-installed code.

Mitigation: Review the package source and extension state before installation, and execute only in an environment where replacing the extension is acceptable.

Risk: The skill stores a WeChat connector token locally.

Mitigation: Restrict local credential file permissions, keep the workspace trusted, and rotate or remove the credential when access is no longer needed.

Risk: The skill uploads the QR image through a CDN flow.

Mitigation: Use the upload only for the short-lived QR code and avoid sharing the generated image beyond the login session.

Risk: The skill restarts the OpenClaw gateway.

Mitigation: Run the workflow during an acceptable maintenance window or confirm that a gateway restart will not interrupt active work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tianheihei002/skills/yq-weixin-connect)
- [WeChat QR code endpoint](https://ilinkai.weixin.qq.com/ilink/bot/get_bot_qrcode?bot_type=3)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces QR-code handling steps, credential-writing guidance, and gateway restart commands.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
