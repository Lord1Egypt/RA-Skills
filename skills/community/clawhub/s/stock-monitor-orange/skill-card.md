## Description: <br>
股票监控分析技能 - 自定义股票池监控、实时行情、技术指标分析、涨跌趋势预测、信号提醒 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xsqorange](https://clawhub.ai/user/xsqorange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users use this skill to monitor A-share and Hong Kong stock watchlists, holdings, trade records, technical indicators, market news, and scheduled market reports. The skill supports manual CLI checks and automated report delivery for portfolio monitoring workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled reports may include holdings, cost basis, profit/loss, or trade history and send them to a Feishu group. <br>
Mitigation: Before enabling scheduled delivery, verify the recipient group, preview the generated report, and remove or redact portfolio and trade details unless that sharing is intentional. <br>
Risk: The skill stores portfolio and trade records under ~/.openclaw on the local machine. <br>
Mitigation: Install only in an environment where local users and backups are controlled, and avoid entering sensitive portfolio details unless local storage is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xsqorange/stock-monitor-orange) <br>
- [Publisher profile](https://clawhub.ai/user/xsqorange) <br>
- [Reference index](references/index.md) <br>
- [Command reference](references/commands.md) <br>
- [Configuration reference](references/config.md) <br>
- [Scheduled tasks reference](references/scheduled-tasks.md) <br>
- [Troubleshooting reference](references/troubleshooting.md) <br>
- [Report templates](reports/templates.md) <br>
- [Cron prompt templates](reports/prompts.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON-backed local configuration, and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local OpenClaw JSON files for watchlists, holdings, trades, alerts, and cron jobs; market data and news are fetched from public finance endpoints.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
