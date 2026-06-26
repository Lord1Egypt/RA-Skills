## Description: <br>
Stock Monitor helps an agent manage stock watchlists, retrieve real-time A-share and Hong Kong market data, analyze technical indicators, track positions and trades, and produce monitoring reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xsqorange](https://clawhub.ai/user/xsqorange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to automate stock quote checks, technical analysis, portfolio tracking, scheduled market reports, and alert-style reporting for A-share and Hong Kong stock monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reports may include private holdings, cost basis, trades, and profit/loss and may be posted to a Feishu group. <br>
Mitigation: Confirm the Feishu destination before enabling scheduled delivery, remove private fields where possible, or use a watchlist-only workflow. <br>
Risk: Position and trade commands can mutate local JSON records used for portfolio reporting. <br>
Mitigation: Back up local OpenClaw stock pool, position, trade, and alert JSON files before using mutating commands. <br>
Risk: Automated technical signals and report guidance can be incomplete or misleading for financial decisions. <br>
Mitigation: Treat generated reports as informational, review source data and assumptions, and avoid relying on the skill as investment advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xsqorange/stock-monitor-xsq) <br>
- [Publisher profile](https://clawhub.ai/user/xsqorange) <br>
- [Command reference](references/commands.md) <br>
- [Configuration reference](references/config.md) <br>
- [Indicator reference](references/index.md) <br>
- [Scheduled tasks reference](references/scheduled-tasks.md) <br>
- [Troubleshooting reference](references/troubleshooting.md) <br>
- [Report prompt templates](reports/prompts.md) <br>
- [Report templates](reports/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, console text, JSON records, and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and update local OpenClaw JSON files for stock pools, positions, trades, alerts, and scheduled tasks.] <br>

## Skill Version(s): <br>
1.2.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
