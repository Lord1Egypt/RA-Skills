## Description:

Guides OpenClaw users through configuring WeCom application messaging, group robot webhooks, customer-message workflows, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to connect OpenClaw with an organization's WeCom tenant for internal notifications, group robot messages, customer-service automation, and approval alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WeCom app secrets, access tokens, and webhook URLs are powerful credentials that can expose organizational messaging channels if shared or logged.

Mitigation: Restrict configuration file permissions, keep credentials out of commits and screenshots, redact them from logs, and rotate them after exposure.

Risk: Customer-message monitoring and automated replies can create privacy and compliance exposure if enabled without organizational approval.

Mitigation: Confirm the organization permits automated monitoring and replies before enabling customer-message workflows.

Risk: The security verdict is suspicious because the guide asks users to configure sensitive messaging credentials without enough security and privacy safeguards.

Mitigation: Review the integration plan with tenant administrators and apply the security guidance before deployment.

## Reference(s):

- [WeCom Admin Console](https://work.weixin.qq.com/wework_admin/frame)
- [WeCom Developer Documentation](https://developer.work.weixin.qq.com/document)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [ClawHub Skill Page](https://clawhub.ai/yang1002378395-cmyk/skills/wecom-quickstart-cn)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with YAML and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides setup, validation, troubleshooting, and pricing guidance in Chinese.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, skill.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
