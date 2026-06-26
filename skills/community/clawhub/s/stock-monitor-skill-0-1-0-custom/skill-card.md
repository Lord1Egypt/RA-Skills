## Description: <br>
A stock monitoring and alerting skill for configured equities, ETFs, and gold instruments, with threshold, volume, moving-average, RSI, gap, and trailing-stop alert rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiden-fan](https://clawhub.ai/user/aiden-fan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure a continuously running market monitor for selected China-market stocks, ETFs, and gold instruments. It helps generate informational alerts and analysis cues, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The monitor can run continuously in the background and poll external financial-data providers. <br>
Mitigation: Review the configured watchlist and stop the daemon when monitoring is no longer needed. <br>
Risk: Queried symbols, names, and watchlist choices may be visible to third-party financial-data providers. <br>
Mitigation: Remove sensitive holdings or replace the hardcoded watchlist with a reviewed local configuration before use. <br>
Risk: Generated alerts and suggestions may be mistaken for financial advice. <br>
Mitigation: Treat the output as informational signals and require independent human review before making trading decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aiden-fan/stock-monitor-skill-0-1-0-custom) <br>
- [Artifact README](README.md) <br>
- [Artifact skill definition](SKILL.md) <br>
- [Eastmoney quote and news APIs](https://push2.eastmoney.com/api/qt/stock/get) <br>
- [Sina finance quote API](https://quotes.sina.cn/cn/api/quotes.php?symbol={code}&source=sina) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and shell command snippets, plus generated market-alert text from the monitor scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run as a local background monitor and query third-party financial-data providers for configured symbols.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
