## Description:

将 WeFlow 导出的微信聊天 JSON 数据转换为个人知识库条目、知识卡片和 AI 分身训练数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[weebrclb123-del](https://clawhub.ai/user/weebrclb123-del)

### License/Terms of Use:

MIT-0

## Use Case:

Users who are authorized to process WeChat exports use this skill to extract customer profiles, business keywords, decisions, communication patterns, and follow-up records from WeFlow JSON chat data. The resulting knowledge cards and Feishu table fields support personal knowledge bases, customer management, and AI persona training preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private WeChat exports and derived customer profiles may include sensitive personal or business information.

Mitigation: Process only chats you are authorized to use, redact sensitive content before creating knowledge cards, and define retention rules for generated files and Feishu records.

Risk: Generated knowledge cards or Feishu tables may expose private conversations if shared too broadly.

Mitigation: Store outputs only in restricted Feishu spaces or local locations with appropriate access controls.

Risk: Extracted summaries, customer profiles, and follow-up records may be incomplete or misleading.

Mitigation: Review generated cards against the source chat export before using them for customer management, contract follow-up, or AI persona training.

## Reference(s):

- [Feishu Knowledge Base Field Design Reference](references/feishu-template.md)
- [ClawHub Skill Page](https://clawhub.ai/weebrclb123-del/skills/wechat-knowledge-builder)
- [Publisher Profile](https://clawhub.ai/user/weebrclb123-del)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown knowledge cards, Feishu table field guidance, and optional Python-generated Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may contain private chat-derived customer details and should be reviewed, redacted, and access-controlled before sharing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
