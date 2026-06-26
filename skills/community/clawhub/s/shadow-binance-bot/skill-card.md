## Description: <br>
Analyze Binance trade history and portfolio data to identify emotional trading patterns and simulate alternative strategies for educational trading insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[acevod](https://clawhub.ai/user/acevod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Traders and developers use this skill to review Binance Spot and Futures history, compare actual trades with simulated alternative strategies, and receive educational coaching about risk management and trading behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses sensitive Binance API credentials to read balances and trading history. <br>
Mitigation: Use read-only Binance API keys, disable trading and withdrawals, restrict keys by IP where possible, and prefer environment variables over config files. <br>
Risk: Strategy simulations and coaching output may be mistaken for financial advice or trading signals. <br>
Mitigation: Treat all simulations as educational estimates and review decisions independently before trading. <br>


## Reference(s): <br>
- [Shadow Binance Bot on ClawHub](https://clawhub.ai/acevod/shadow-binance-bot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, API Calls] <br>
**Output Format:** [Markdown-style trading analysis, simulation summaries, and coaching guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses read-only Binance API credentials when configured; demo mode can run without real account access.] <br>

## Skill Version(s): <br>
1.3.3 (source: server release evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
