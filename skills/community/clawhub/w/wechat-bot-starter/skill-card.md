## Description:

Helps developers quickly scaffold WeChat bots using Wechaty or itchat for auto-replies, message monitoring, group management, forwarding, scheduled messages, and optional OpenClaw integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to create starter WeChat bot implementations, compare Wechaty, itchat, Enterprise WeChat, and ComWechat options, and add common automation patterns such as auto-replies, group handling, forwarding, scheduled messages, and OpenClaw-backed responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chat access, message monitoring, and forwarding can expose sensitive conversation content.

Mitigation: Use a dedicated bot account where possible, limit the bot to intended chats, and get consent before monitoring or forwarding messages.

Risk: Automated sending can create abuse, spam, or account-enforcement risk.

Mitigation: Add rate limits, keep logs, avoid unintended marketing content, and review behavior before deployment.

Risk: Unpinned dependencies or an exposed OpenClaw chat endpoint can create supply-chain or access-control risk.

Mitigation: Review and pin dependencies, and keep the OpenClaw endpoint local or protect remote access with authentication and HTTPS.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yang1002378395-cmyk/skills/wechat-bot-starter)
- [Publisher Profile](https://clawhub.ai/user/yang1002378395-cmyk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell, JavaScript, Python, and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and npm for the Wechaty examples; Python examples use itchat and related packages.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
