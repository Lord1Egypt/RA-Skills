## Description: <br>
股票盯盯 is a stock monitoring and alerting skill for China-market stocks, ETFs, and gold, with configurable cost, price-change, volume, moving-average, RSI, gap, and trailing-stop rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[koradji77](https://clawhub.ai/user/koradji77) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure watchlists, run scheduled stock monitoring, and receive informational Feishu alerts and closing summaries. It supports repeated monitoring workflows but its alerts should not be treated as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store configured stock symbols, costs, alerts, cached closing data, and behavior-analysis history under the skill directory. <br>
Mitigation: Review local data files before sharing or publishing the workspace, and avoid configuring sensitive holdings unless local storage is acceptable. <br>
Risk: The release evidence warns that the default Feishu target should be replaced or removed before installation. <br>
Mitigation: Set the intended Feishu recipient before running alerts, or disable Feishu delivery until the target is confirmed. <br>
Risk: Stock alerts and generated summaries can be mistaken for trading advice. <br>
Mitigation: Treat all alerts as informational signals and review them with independent financial judgment. <br>
Risk: Scheduled cron or background monitoring can run repeatedly and send recurring notifications. <br>
Mitigation: Review any cron entries and background process controls before enabling long-running monitoring. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/koradji77/stock-watcher-cn) <br>
- [README](artifact/README.md) <br>
- [Quick start guide](artifact/快速开始.md) <br>
- [User guide](artifact/用户指南.md) <br>
- [Detailed usage guide](artifact/股票盯盯详细使用说明.md) <br>
- [Test instructions](artifact/测试说明.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python configuration snippets, shell commands, and alert message text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local watchlist, alert, cache, and behavior-analysis data when configured and run.] <br>

## Skill Version(s): <br>
4.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
