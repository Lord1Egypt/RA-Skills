## Description:

小红薯数据日报提供小红书公开笔记、评论和博主数据的只读查询，并以结构化 JSON 输出，供 AI 汇总分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT

## Use Case:

创作者、运营团队、品牌和内容分析人员可用它查询小红书公开笔记、评论及博主互动数据，整理选题、竞品表现和舆情日报或周报。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and note or creator links are sent to the third-party API provider.

Mitigation: Send only queries and links that are appropriate to share with the provider; avoid sensitive or identifying material.

Risk: The security scan has medium confidence and incomplete interpretation for 13 files.

Mitigation: Review the skill source before use and limit the token and data supplied to what the task requires.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/guaikei/skills/xhs-brief)
- [GuaiKei API service](https://www.guaikei.com)
- [Output contract](artifact/references/contract.md)
- [Command routing](artifact/references/routing.md)
- [Output envelope schema](artifact/assets/output_envelope.schema.json)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON response envelope]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Contains public note search results, note details, comments, or creator metrics for downstream summaries and reports.]

## Skill Version(s):

1.2.3 (source: SKILL.md frontmatter, package.json, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
