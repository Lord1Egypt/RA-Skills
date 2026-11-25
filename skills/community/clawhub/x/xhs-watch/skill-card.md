## Description:

小红薯舆情监控数据源（只读）：关键词搜笔记、爆款选题、笔记详情、评论舆情与博主作品，输出结构化 JSON，不登录或发布。

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT-0

## Use Case:

内容运营、品牌与客服团队可用它检索小红书公开笔记、读取单篇内容与评论、查看博主作品及互动数据，并将结构化结果用于选题、竞品观察和口碑分析。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and note links may contain sensitive information sent to the service; the security scan also reports incomplete inspection and degraded tool-misuse analysis.

Mitigation: Avoid sending sensitive terms or links, and review the service's data-sharing and support guidance before use. Treat the scan's suspicious verdict as a reason for caution, not as a conclusion that the publisher is malicious.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guaikei/skills/xhs-watch)
- [Guaikei service](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public Xiaohongshu search, note, comment, and creator data; query limits depend on the service plan.]

## Skill Version(s):

1.2.3 (source: ClawHub release, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
