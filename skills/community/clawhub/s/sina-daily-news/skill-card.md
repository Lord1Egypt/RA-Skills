## Description:

抓取新浪财经 7x24 实时新闻流，自动分类生成结构化日报；每类新闻按时间线排列，标注来源和阅读量，适合每日早间财经、政治、科技新闻速览。

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch public Sina Finance 7x24 news text and turn it into a concise Chinese Markdown daily report grouped by topic. It is suited for recurring morning briefings that need time, source, and readership details preserved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional cron example runs daily and may persist reports to memory.

Mitigation: Review the cron schedule, destination, and retained report contents before enabling automated execution.

Risk: News parsing and keyword classification can omit items or place them in the wrong category when the source page format or wording changes.

Mitigation: Review generated reports before relying on them and update category keywords or parsing rules when output quality drifts.

Risk: The report depends on public Sina Finance content fetched at runtime.

Mitigation: Cross-check important stories with additional sources when accuracy, completeness, or availability matters.

## Reference(s):

- [Sina Finance 7x24 News](https://finance.sina.com.cn/7x24/?tag=0)
- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/sina-daily-news)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Configuration]

**Output Format:** [Chinese Markdown report with categorized news sections and optional cron configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can read fetched news text from stdin or a command-line argument; optional cron usage may save daily reports to memory.]

## Skill Version(s):

1.0.0 (source: SKILL.md metadata, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
