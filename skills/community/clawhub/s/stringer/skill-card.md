## Description:

「什么值得做」(stringers.io):每天更新的判断,现在哪些小产品方向正在爆、钱流向谁、窗口开到什么时候,约 90 个方向每个一篇查过 15 个数据库的长文加评级。用户问「现在做什么」「这个想法有没有搞头」「谁在做 X、赚到钱没」「今天有什么新机会」、要一份按他情况筛过的日报、或在自己的项目里问方向对不对,就用它。

This skill is ready for commercial/non-commercial use.

## Publisher:

[komako-workshop](https://clawhub.ai/user/komako-workshop)

### License/Terms of Use:

MIT-0

## Use Case:

希望寻找或评估小型产品机会的创业者和产品团队，可用此技能查看市场方向、收入信号与评级，并根据自身情况获取机会建议或每日简报。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Questions sent through the external MCP service include a short summary; its implementation and data retention practices have not been reviewed.

Mitigation: Keep confidential project details out of MCP queries. Use the public JSON route for local personalization, and save profile or preference details only with the user's agreement.

## Reference(s):

- [Stringers](https://stringers.io)
- [Stringers daily briefing JSON](https://stringers.io/api/today.json)
- [Stringers opportunity data JSON](https://stringers.io/api/all.json)
- [Stringers data status](https://stringers.io/status.json)
- [ClawHub skill release](https://clawhub.ai/komako-workshop/skills/stringer)

## Skill Output:

**Output Type(s):** [Analysis, Text, Guidance]

**Output Format:** [Markdown recommendations and briefings with ratings, dated figures, sources, and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May tailor recommendations to user-provided preferences and profile.]

## Skill Version(s):

0.2.0 (source: frontmatter, server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
