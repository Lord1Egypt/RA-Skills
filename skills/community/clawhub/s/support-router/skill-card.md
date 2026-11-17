## Description:

客服邮件智能分流技能，通过 CLI 关键词预筛自动回复常见定价和取消订阅邮件，并将商务、Bug 或未分类邮件转发给人工邮箱或 AI 处理邮箱。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devincodel](https://clawhub.ai/user/devincodel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and independent SaaS operators use this skill to set up scheduled support email triage that answers FAQ-style pricing and cancellation messages with templates, forwards business messages to a human inbox, and sends complex or unknown cases to an AI-assisted support mailbox for analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled mailbox processing can execute shell-string commands built from email, message, and configuration values.

Mitigation: Replace shell-string execSync calls with argument-array execution and validate email addresses, message IDs, and configuration values before use.

Risk: The mail-cli lookup can fall back to dynamic npx package execution.

Mitigation: Remove the npx fallback and require a pinned, preinstalled mail-cli binary from a trusted source.

Risk: Forwarded complex messages give the AI mailbox authority to send reports based on public inbound email.

Mitigation: Restrict csbot to one approved reporting action and recipient, and operate it with a least-privileged mailbox or account.

Risk: Generated channel install commands can change runtime behavior and restart OpenClaw.

Mitigation: Validate any generated channel install command before running it and install the csbot channel only after configuration and tests are complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/devincodel/skills/support-router)
- [Publisher profile](https://clawhub.ai/user/devincodel)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples, shell commands, and JavaScript router code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mail-cli, Node.js, and a scheduled runner such as cron or OpenClaw schedule.]

## Skill Version(s):

1.0.12 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
