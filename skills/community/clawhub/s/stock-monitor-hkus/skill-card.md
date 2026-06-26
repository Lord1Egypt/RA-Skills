## Description: <br>
港股/美股/加密货币实时监控，使用 Yahoo Finance (yfinance) 获取实时价格和技术指标，支持自定义股票池、涨跌提醒、均线/RSI/MACD信号。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sanduan003](https://clawhub.ai/user/sanduan003) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to monitor selected Hong Kong stocks, U.S. stocks, and cryptocurrency prices, then review technical indicators such as moving averages, RSI, and MACD signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The monitor writes a local state file to a hard-coded path, which may fail or disclose local monitoring data on some systems. <br>
Mitigation: Review and change the state-file path before scheduled or repeated use. <br>
Risk: The quick-start dependency command uses --break-system-packages, which can affect the system Python environment. <br>
Mitigation: Install dependencies in a Python virtual environment instead. <br>
Risk: A cron entry can create periodic background market monitoring. <br>
Mitigation: Add scheduled execution only when ongoing background monitoring is intended. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and terminal text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled monitor script writes a local JSON state file when run.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
