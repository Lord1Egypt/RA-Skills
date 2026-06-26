## Description: <br>
T+0 基金 5 分钟级别实时监控，支持批量代码输入，自动生成买入/卖出信号。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newhackerman](https://clawhub.ai/user/newhackerman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to manage a local watchlist of A-share T+0 fund or ETF codes, monitor market data during trading hours, and surface informational buy/sell signals from MACD, KDJ, RSI, Bollinger Band, and volume indicators. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs Python market-data and scheduling dependencies from pip. <br>
Mitigation: Install in a controlled Python environment and review the declared requirements before use. <br>
Risk: The skill stores fund codes, logs, and simulated trade history under the fund-monitor skill directory. <br>
Mitigation: Restrict access to the skill data directory and clean local data when it is no longer needed. <br>
Risk: Optional DingTalk or WeChat notifications can send signal details through external webhook channels. <br>
Mitigation: Enable webhooks only for trusted channels and protect webhook secrets in configuration. <br>
Risk: Generated buy/sell signals can be mistaken for investment advice. <br>
Mitigation: Treat signals as informational, account for market-data delay, and make investment decisions independently. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/newhackerman/t0-fund-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/newhackerman) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and terminal text with inline shell commands and YAML configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local watchlist, signal, trade history, PID, and log files under the fund-monitor skill directory when commands are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
