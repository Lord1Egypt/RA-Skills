## Description: <br>
Query stock quotes and technical analysis for A-share, Hong Kong, and U.S. stocks, returning real-time quote data, RSI/MACD indicators, a buy/sell/hold signal, and a trend chart image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dongdong-bryant](https://clawhub.ai/user/dongdong-bryant) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to request stock-code summaries across supported A-share, Hong Kong, and U.S. markets. It fetches market data, computes simple technical indicators, and prepares a readable quote summary with a one-month trend chart. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested stock symbols are sent to external finance data providers. <br>
Mitigation: Use only stock symbols you are comfortable sharing with the configured market data providers. <br>
Risk: The buy/sell/hold signal may be mistaken for financial advice. <br>
Mitigation: Treat the signal as a simple RSI/MACD technical indicator and review it independently before making trading decisions. <br>
Risk: The generated chart image may overwrite an existing stock_chart.png file in the workspace. <br>
Mitigation: Move or rename any existing chart output before running the skill when file preservation matters. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Guidance] <br>
**Output Format:** [Plain text stock summary plus a generated PNG chart image] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Takes one stock code as input and may overwrite the stock_chart.png chart output in the OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
