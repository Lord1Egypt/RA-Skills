## Description:

只读检索小红书公开笔记、评论和博主数据，并以结构化 JSON 输出，支持内容选题、竞品分析、KOL 筛选和舆情分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[um-why](https://clawhub.ai/user/um-why)

### License/Terms of Use:

MIT-0

## Use Case:

创作者、运营人员、品牌团队和分析人员可用它搜索小红书公开笔记、查看笔记详情与评论，或获取博主作品及公开互动数据，以支持选题、竞品、KOL 和舆情分析。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Keywords and links supplied for queries may be sent to the Guaikei service; the security assessment flags privacy and tool-scope concerns.

Mitigation: Use non-sensitive keywords and public links, and account for third-party processing before querying.

Risk: The security assessment gives a suspicious verdict with medium confidence and reports incomplete component inspection (69%).

Mitigation: If greater assurance is needed, wait for clearer tool-scope and data-sharing information, following the supplied security guidance.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/um-why/skills/xhs-content-analytics)
- [Guaikei data service](https://www.guaikei.com)
- [Usage contract](references/contract.md)
- [Command options](references/options.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public data results for search, note details, comments, and blogger profiles or posts.]

## Skill Version(s):

1.2.2 (source: SKILL.md frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
