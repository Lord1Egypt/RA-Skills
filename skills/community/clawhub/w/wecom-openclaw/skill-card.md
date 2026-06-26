## Description: <br>
Integrate WeChat Work (Enterprise WeChat) with OpenClaw for intelligent messaging, receiving messages from WeChat Work, processing them with Claude AI, and sending async replies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richagain](https://clawhub.ai/user/richagain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and administrators use this skill to deploy and configure a WeChat Work webhook adapter that forwards text messages to OpenClaw and sends asynchronous replies back through the WeChat Work API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Business chat contents may be routed through OpenClaw without sufficiently narrow scope or user disclosure. <br>
Mitigation: Install only with organizational approval, disclose the webhook behavior to administrators and affected users, and restrict which users or chats are routed. <br>
Risk: Webhook, WeChat Work, and OpenClaw credentials are required and could expose messaging systems if leaked. <br>
Mitigation: Store secrets outside source control with tight file permissions, rotate any leaked credentials, and review logs for accidental secret exposure. <br>
Risk: Automated replies can send sensitive or inappropriate generated content back into business chats. <br>
Mitigation: Review the security guidance before deployment and add response filtering, rate limits, and monitoring appropriate for the organization. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/richagain/wecom-openclaw) <br>
- [Setup Guide](references/setup-guide.md) <br>
- [Security Guide](references/security-guide.md) <br>
- [WeChat Work](https://work.weixin.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands, JavaScript adapter code, and environment configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces deployment steps and local adapter files for a WeChat Work to OpenClaw bridge.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
