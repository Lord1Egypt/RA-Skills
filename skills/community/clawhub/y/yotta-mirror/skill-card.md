## Description:

学情分析（元镜）—— 把成绩 / 答题表与题目-知识点映射，变成可复算、可追溯的诊断报告：数据质量闸门、逐题统计、按分值加权的知识点掌握率、A/B/C 分层与临界生识别、薄弱点诊断（低样本自动降级为人工复核），支持阈值配置、学生标识匿名化与 CI 闸门；零依赖本地运行，不联网、不调用模型，不用于学生评价或排名。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yottameta](https://clawhub.ai/user/yottameta)

### License/Terms of Use:

MIT-0

## Use Case:

Teachers and education teams use this local analysis tool to turn structured score sheets and item-to-knowledge maps into reproducible learning diagnostics, with evidence and review flags for low-sample or borderline findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Student identities or sensitive details may remain identifiable in reports, even when --anonymize is used.

Mitigation: Use independently assigned random student codes or remove student-level details, then inspect the report before sharing.

Risk: Low-sample conclusions may be unreliable.

Mitigation: Manually review low-sample conclusions and borderline findings before using them.

Risk: A release downloaded by the unpinned npm install command is not covered by inspection of the bundled files.

Mitigation: Review local installation files, preview one destination with --dry-run, and back up customized installations.

## Reference(s):

- [Data format](references/data-format.md)
- [Report format](references/report-format.md)
- [Privacy guidance](references/privacy.md)
- [yotta-mirror project homepage](https://github.com/YottaMeta/yotta-mirror)
- [ClawHub release page](https://clawhub.ai/yottameta/skills/yotta-mirror)

## Skill Output:

**Output Type(s):** [Analysis, Markdown reports, JSON reports, Template files]

**Output Format:** [Markdown and JSON reports; CSV and JSON input templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deterministic local results; low-sample and borderline findings are marked for human review.]

## Skill Version(s):

0.1.3 (source: SKILL.md frontmatter, CHANGELOG.md, package.json; released 2026-11-05)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
