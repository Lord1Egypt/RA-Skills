## Description:

股票监控分析技能 - 自定义股票池监控、实时行情、技术指标分析、涨跌趋势预测、信号提醒

This skill is ready for commercial/non-commercial use.

## Publisher:

[xsqorange](https://clawhub.ai/user/xsqorange)

### License/Terms of Use:

MIT-0

## Use Case:

External users and investors use this skill with OpenClaw to monitor custom A-share and Hong Kong stock pools, manage local positions and trades, generate technical analysis, alerts, and market reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores portfolio positions and trade history in local plaintext JSON files.

Mitigation: Use it only on trusted machines and avoid entering sensitive holdings unless local file access and backups are acceptable.

Risk: The skill may send reports containing holdings and profit or loss details to a Feishu group.

Mitigation: Configure the recipient deliberately, test delivery manually, and avoid scheduled delivery until the destination is verified.

Risk: The skill provides stock signals and trading suggestions that may be incorrect or stale.

Mitigation: Independently verify market data and treat the reports as informational rather than investment advice.

Risk: The skill makes outbound requests to market-data and news providers.

Mitigation: Run it only where those network calls are expected and permitted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xsqorange/skills/stock-monitor-orange)
- [Reference index](references/index.md)
- [Commands](references/commands.md)
- [Configuration](references/config.md)
- [Scheduled tasks](references/scheduled-tasks.md)
- [Troubleshooting](references/troubleshooting.md)
- [Report templates](reports/templates.md)
- [Cron prompt templates](reports/prompts.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON-style analysis output, and CLI command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local plaintext JSON configuration and portfolio files; may make outbound market-data requests and send reports to Feishu when configured.]

## Skill Version(s):

1.0.10 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
