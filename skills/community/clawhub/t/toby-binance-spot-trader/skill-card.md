## Description: <br>
Autonomous Binance spot trading bot that uses technical indicators and LLM sentiment analysis to support momentum, mean reversion, and DCA strategies on Binance spot pairs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure and run an automated Binance spot trading workflow, monitor account balances, and apply momentum, mean reversion, or DCA strategies with optional LLM sentiment filtering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically place real Binance market orders with real funds and no built-in confirmation or paper-trading default. <br>
Mitigation: Do not run it on a live account until paper trading or testnet support, explicit live-trading opt-in, and hard risk limits are added or verified. <br>
Risk: The skill requires sensitive Binance and SkillBoss credentials. <br>
Mitigation: Use Binance API keys with withdrawals disabled, IP restrictions, limited funds in a sub-account, and secure local storage for environment files. <br>
Risk: The LLM sentiment step sends trading context to the SkillBoss/HeyBoss endpoint. <br>
Mitigation: Confirm that the endpoint is trusted for the trading context before enabling LLM filtering. <br>


## Reference(s): <br>
- [Binance REST API Reference](references/binance-api.md) <br>
- [Technical Indicators](references/indicators.md) <br>
- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/toby-binance-spot-trader) <br>
- [Metadata homepage](https://github.com/srikanthbellary) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands, environment-variable configuration, and Python scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local setup guidance, trading and portfolio scripts, and runtime logs/trade records when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
