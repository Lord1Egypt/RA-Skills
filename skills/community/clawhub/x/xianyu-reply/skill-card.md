## Description:

闲鱼自动回复助手帮助用户配置并运行闲鱼（Goofish）消息监控和 AI 自动回复服务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[sinabs](https://clawhub.ai/user/sinabs)

### License/Terms of Use:

MIT-0

## Use Case:

External marketplace sellers use this skill to set up a local helper that monitors Goofish buyer messages, drafts short AI replies from item and conversation context, and sends replies automatically.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for a full Goofish browser Cookie and stores it in plaintext local configuration.

Mitigation: Use a dedicated low-risk account, keep the configuration file private, rotate the Cookie if exposed, and remove the file when the service is no longer needed.

Risk: AI-written marketplace replies can be sent automatically without human approval.

Mitigation: Review behavior with low-risk conversations first, monitor logs, and use the documented manual handoff control when a conversation needs human review.

Risk: Buyer messages, item details, and conversation history are passed to the configured local AI CLI/provider.

Mitigation: Confirm the privacy posture of the selected AI CLI/provider before use and avoid processing sensitive buyer or account information.

## Reference(s):

- [闲鱼 Cookie 获取指南](references/cookie_guide.md)
- [Goofish web site](https://www.goofish.com)
- [ClawHub skill release](https://clawhub.ai/sinabs/skills/xianyu-reply)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides local setup, dependency installation, cookie configuration, background service management, and AI reply behavior.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
