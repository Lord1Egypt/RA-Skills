## Description:

港股/美股/加密货币实时监控。使用 Yahoo Finance (yfinance) 获取实时价格、技术指标监控。支持自定义股票池、涨跌提醒、均线/RSI/MACD信号。

This skill is ready for commercial/non-commercial use.

## Publisher:

[sanduan003](https://clawhub.ai/user/sanduan003)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to monitor configured Hong Kong, U.S., and cryptocurrency tickers, review price changes and technical signals, and optionally run the monitor on a schedule.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented install command can modify system Python packages.

Mitigation: Review the script before installation and install yfinance and numpy in a virtual environment with pinned dependency versions.

Risk: The monitor writes state to a hard-coded local path that differs from the documented relative path.

Mitigation: Change the state output path to an expected workspace location or verify the directory exists and has appropriate permissions before running the script.

Risk: Running the monitor contacts Yahoo Finance for the configured ticker symbols.

Mitigation: Use it only in environments where sending those ticker lookups to Yahoo Finance is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sanduan003/skills/stock-monitor-hkus)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, code]

**Output Format:** [Terminal text output with setup and scheduling commands; runtime state is JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Configured tickers are defined in scripts/monitor.py; no credential environment variables were detected.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
