## Description: <br>
企业微信快速集成配置 helps connect OpenClaw with Enterprise WeChat for group bot messages, application messages, and customer management workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure OpenClaw for Enterprise WeChat messaging, group bot notifications, customer-service automation, and approval notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Enterprise WeChat credentials, webhook URLs, and OpenClaw configuration may expose tenant messaging capabilities if stored or shared insecurely. <br>
Mitigation: Use least-privilege WeCom apps, restrict visible departments and recipients, protect ~/.openclaw/config.yml from other users and source control, and rotate exposed secrets. <br>
Risk: Customer-message automation can send unintended or inaccurate replies if enabled broadly before validation. <br>
Mitigation: Test auto-replies in a limited group before using them with customers and govern customer-message automation according to internal policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/wecom-quickstart-cn) <br>
- [Enterprise WeChat admin console](https://work.weixin.qq.com/wework_admin/frame) <br>
- [Enterprise WeChat developer documentation](https://developer.work.weixin.qq.com/document) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration, Shell commands] <br>
**Output Format:** [Markdown with YAML and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for webhook testing; may include Enterprise WeChat credential placeholders for user-supplied configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
