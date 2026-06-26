## Description: <br>
Run trading strategy backtests with natural language, powered by Vynn. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beee003](https://clawhub.ai/user/beee003) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to submit natural language or structured trading strategies to Vynn and receive backtest metrics such as Sharpe ratio, return, drawdown, win rate, trade count, and equity curve information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Strategy descriptions, ticker lists, and lookback settings are sent to Vynn for backtest execution. <br>
Mitigation: Avoid including sensitive portfolio, account, or personal financial details in prompts and review inputs before running a backtest. <br>
Risk: The skill requires a VYNN_API_KEY and supports overriding VYNN_BASE_URL. <br>
Mitigation: Use a dedicated API key and verify any VYNN_BASE_URL override before use. <br>


## Reference(s): <br>
- [Vynn homepage](https://the-vynn.com) <br>
- [Vynn backtest endpoint](https://the-vynn.com/v1/backtest) <br>
- [ClawHub release page](https://clawhub.ai/beee003/vynn-backtester) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration] <br>
**Output Format:** [Markdown examples and structured backtest result text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VYNN_API_KEY and sends strategy inputs to the configured Vynn API endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
