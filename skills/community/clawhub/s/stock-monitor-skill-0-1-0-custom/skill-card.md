## Description:

A Chinese-language stock monitoring and alerting skill for A-shares, ETFs, and gold that checks cost percentage, intraday movement, volume, moving-average crosses, RSI, gaps, and trailing-stop signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiden-fan](https://clawhub.ai/user/aiden-fan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor configured China-market stock, ETF, and gold positions and receive rule-based alert messages with concise market context. Its alerts and suggestions are informational and should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run as a local background process and write monitoring logs under ~/.stock_monitor.

Mitigation: Start it only in an environment where a persistent local watcher is expected, review logs periodically, and stop it with the bundled control command when monitoring is no longer needed.

Risk: Configured watchlist symbols are sent to external market-data and news services.

Mitigation: Avoid placing sensitive portfolio information in the watchlist and review the external services before using the skill in a restricted environment.

Risk: Stock alerts and generated suggestions may be incomplete, stale, or unsuitable for trading decisions.

Mitigation: Treat outputs as informational signals and verify them against trusted market data and personal investment criteria before acting.

Risk: The security guidance notes quality and hardening issues around endpoint and PID validation.

Mitigation: Harden endpoint handling and PID validation before relying on the skill for long-running or higher-trust workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aiden-fan/skills/stock-monitor-skill-0-1-0-custom)
- [Eastmoney stock data endpoints](https://push2his.eastmoney.com/api/qt/stock/kline/get)
- [Sina finance quote endpoint](https://hq.sinajs.cn/list={codes})

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-like alert text with shell command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run as a local background process and write logs under ~/.stock_monitor when started by the user.]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
