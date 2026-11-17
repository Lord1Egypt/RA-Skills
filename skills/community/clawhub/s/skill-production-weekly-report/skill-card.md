## Description:

生产管理周报生成工具；将口头描述、Word/Excel数据解析为结构化HTML周报，支持4周历史追踪，数据不足时自动拒绝。

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Production managers and operations teams use this skill to turn spoken updates, Word documents, Excel workbooks, and recent report history into a structured weekly production report. The skill validates required inputs before generation and refuses to create a report when core metrics, completed work, or next-week plans are missing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML report output can preserve injected markup from Word, Excel, JSON, or transcribed input values.

Mitigation: Review before installing, use only trusted report inputs, or add HTML escaping before publishing or sharing generated reports.

Risk: The skill reads user-specified local files and saves persistent report copies under weekly_reports/history.

Mitigation: Limit input paths to expected report files and review generated history files before distribution.

## Reference(s):

- [Production weekly report format specification](references/report_format.md)
- [Server-resolved GitHub provenance](https://github.com/duding-engicool/skill-production-weekly-report)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-production-weekly-report)
- [ClawHub publisher profile](https://clawhub.ai/user/duding-engicool)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands; JSON parser output and saved HTML weekly report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads user-specified Word, Excel, JSON, and history files; writes reports under weekly_reports/ and weekly_reports/history/.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
