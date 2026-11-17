## Description:

亚协体育瑜伽馆经营知识库读取技能，用于搜索、读取和总结瑜伽馆经营知识，包括销售话术、活动策划、团队管理、股权合伙、抖音运营、私教成交、会员运营和卡项设计等内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[design84086505-maker](https://clawhub.ai/user/design84086505-maker)

### License/Terms of Use:

MIT-0

## Use Case:

External operators, consultants, and agent users can use this skill to query a Feishu-hosted yoga studio operations knowledge base and produce concise answers or summaries for sales, campaigns, staffing, partnerships, legal-contract topics, and member operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Published Feishu app credentials could allow unauthorized access to tenant knowledge-base resources.

Mitigation: Revoke and rotate the secret, remove it from all published files and history, and require protected runtime secret injection before use.

Risk: Over-broad Feishu access could expose documents beyond the intended knowledge-base space.

Mitigation: Confirm the app has read-only least-privilege access limited to the intended knowledge-base space.

Risk: Object-token exposure and user-selected output paths can increase data leakage or file-write risk.

Mitigation: Restrict or remove object-token exposure and constrain output paths before deployment.

## Reference(s):

- [亚协知识库文件索引](artifact/references/file_index.md)
- [ClawHub Skill Page](https://clawhub.ai/design84086505-maker/skills/yaxie-yoga-studio-consultant)
- [Publisher Profile](https://clawhub.ai/user/design84086505-maker)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain text with optional inline shell commands and extracted knowledge-base text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file names, object tokens, extracted document excerpts, and summarized operating guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
