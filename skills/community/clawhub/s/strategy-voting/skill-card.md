## Description: <br>
Strategy Voting combines breakout, RSI mean reversion, MACD crossover, and Bollinger Band signals into a weighted trading-signal vote. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huiLI203](https://clawhub.ai/user/huiLI203) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-bot operators use this skill to generate local technical-analysis signals and reports for strategy filtering. Its output should be reviewed before any trading decision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading signals can be wrong and may contribute to financial loss if treated as automatic trading instructions. <br>
Mitigation: Use the output as a local signal aid only, and require explicit confirmation, position sizing, stop-loss rules, and independent review before live trading. <br>
Risk: The included command-line run prints a report from generated sample data, not live market data. <br>
Mitigation: Confirm the input data source before relying on a report for strategy filtering or downstream automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huiLI203/strategy-voting) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text report with shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires price and volume data when used as a library; the included command-line run uses generated sample data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
