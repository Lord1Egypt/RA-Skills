## Description:

根据公众号名称或链接，归纳公众号定位和核心观点，帮用户选择关键词偏好并定时推送聚合内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuchenggong19851114-design](https://clawhub.ai/user/zhuchenggong19851114-design)

### License/Terms of Use:

MIT-0

## Use Case:

Users who follow WeChat public accounts use this skill to summarize an account's positioning, core viewpoints, and follow value, then receive scheduled topic-based content digests. It can remember selected keyword preferences and save approved summaries to a Feishu aggregation library.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may remember selected content keywords and use them for scheduled daily pushes.

Mitigation: Use it only when users are comfortable storing those preferences, and let users update or avoid saved preferences when needed.

Risk: The skill can save aggregation results to Feishu, which may preserve user-selected content records.

Mitigation: Create Feishu records only after explicit user confirmation, matching the documented workflow and security guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhuchenggong19851114-design/skills/zhuchenggong-wechat-account-aggregation)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise Chinese prose or Markdown summarizing account positioning, core viewpoints, and follow value.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use remembered keyword preferences for scheduled pushes; Feishu records are created only after user confirmation.]

## Skill Version(s):

1.0.0 (source: evidence.release.version, released 2026-03-26)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
