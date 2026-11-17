## Description:

自动抓取淘股吧“今日推荐”前N个帖子内容，并整理整体行情、板块表现与多数作者观点总结。

This skill is ready for commercial/non-commercial use.

## Publisher:

[guowei-xie](https://clawhub.ai/user/guowei-xie)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-speaking users use this skill to collect and summarize Taoguba “今日推荐” posts into a readable A-share market review. It is intended for objective digestion of forum authors' stated views, not for adding independent investment recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may log in to Taoguba using user-provided credentials.

Mitigation: Use a dedicated or low-privilege account when possible, avoid password reuse, provide credentials only through environment variables, and clear them after use.

Risk: Fetched posts may include account-gated or private material.

Mitigation: Review generated URL and content files before sharing summaries or downstream artifacts.

Risk: Forum post summaries about A-share markets can be mistaken for investment advice.

Mitigation: Present the output as a digest of source authors' views and avoid adding independent trading recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guowei-xie/skills/taoguba-picks-digest)
- [Taoguba](https://www.tgb.cn/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summary with headings, tables, and concise narrative sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries should preserve source authors' views, avoid extra market judgment, and may include focus stocks mentioned across posts.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
