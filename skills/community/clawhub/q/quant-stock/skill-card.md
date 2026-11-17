## Description:

AI量化选股系统 - 基于多维度评分模型的A股选股分析工具。扫描新能源、电力、半导体、医药、AI、机器人、军工、贵金属等行业，输出每日量化选股报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[rix-zhang](https://clawhub.ai/user/rix-zhang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to scan A-share stock pools across target industries, score candidates with technical, market, theme, news, and industry-selection signals, and generate daily stock-selection reports for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports may be sent to hard-coded Feishu recipients or external channels.

Mitigation: Replace hard-coded Feishu targets with explicit user configuration and provide Feishu/OpenClaw credentials only after approving external delivery.

Risk: The cron installer can create recurring scheduled execution.

Mitigation: Review the cron jobs before installation and run the installer only when persistent weekday and weekly execution is intended.

Risk: Runtime dependency installation is not pinned and may change execution behavior over time.

Mitigation: Pin dependencies and move package installation into a deliberate setup step before scheduled runs.

## Reference(s):

- [Scoring Rules](references/RULES.md)
- [ClawHub Skill Page](https://clawhub.ai/rix-zhang/skills/quant-stock)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style daily stock report with ranked picks, scores, tags, industry summary, setup commands, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write daily_report.txt and can deliver reports to Feishu when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
