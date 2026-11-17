## Description:

搜索小红书公开笔记、查看笔记详情与评论，并读取博主公开作品和互动数据，供趋势调研与内容分析使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

内容创作者、品牌团队和研究人员可用关键词发现公开笔记趋势，并根据笔记或主页链接查看详情、评论和博主互动数据，以支持选题、竞品观察和评论归纳。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and Xiaohongshu links are sent to the Guaikei service, and successful results may be saved in local temporary logs.

Mitigation: Avoid submitting sensitive query details or links. Set XHS_GUAIKEI_DISABLE_LOG=1 to disable local result logging, or remove the dated logs when finished.

Risk: ClawScan reports medium confidence and incomplete inspection of some JavaScript files; its benign verdict is not a guarantee of safety.

Mitigation: Review the skill and its JavaScript files before installation and decide whether the service and local logging behavior fit your use.

## Reference(s):

- [Service website](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Troubleshooting reference](references/troubleshooting.md)
- [Changelog](references/changelog.md)
- [Support issues](https://github.com/um-why/xiaohongshu-openclaw-skill/issues)
- [ClawHub release page](https://clawhub.ai/why20261/skills/xiaohongshu-notes-search)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON envelope containing public note search results, note details, comments, or creator data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public data only; request limits depend on the token plan, and results may be saved in the system temporary directory.]

## Skill Version(s):

1.2.1 (source: server-resolved release metadata, SKILL.md, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
