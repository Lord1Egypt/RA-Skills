## Description:

基于 trumpstruth.org/feed 汇总特朗普相关公开推文（RSS），按 Evidence、Latest 和 Time 模式输出证据与金融教育分析，并以特朗普口吻进行对话。

This skill is for research and development only.

## Publisher:

[vialiceq](https://clawhub.ai/user/vialiceq)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to review public Trump-related RSS items and receive educational market-context analysis, observation lists, and scenario discussion. It is intended for evidence-grounded financial education rather than personalized trading advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persona-style responses may be mistaken for authentic statements or investment advice.

Mitigation: Treat Trump-style commentary as simulated output, keep risk notices visible, and verify market-relevant claims against primary sources before acting.

Risk: Financial education analysis may be misused as individualized trading guidance.

Mitigation: Use observation lists and scenario discussion instead of buy/sell instructions, and redirect direct trading requests to risk discussion.

Risk: RSS availability or feed parsing issues may affect evidence quality.

Mitigation: Base evidence mode only on displayed RSS items and avoid claiming source details that are not shown in the extracted evidence.

## Reference(s):

- [Trump Truth RSS feed](https://www.trumpstruth.org/feed)
- [ClawHub skill page](https://clawhub.ai/vialiceq/skills/trump-invest)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Markdown-style response with RSS evidence items, educational financial analysis, observation lists, scenario discussion, and risk notices]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Evidence and latest modes select 2-5 RSS items when available; responses must avoid personalized buy/sell instructions and profit guarantees.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
