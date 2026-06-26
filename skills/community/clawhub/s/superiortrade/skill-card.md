## Description: <br>
Backtest and deploy trading strategies on Superior Trade's managed cloud. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[superior-ai](https://clawhub.ai/user/superior-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trading-strategy developers use this skill to design, backtest, tune, and deploy crypto trading strategies on Superior Trade, including dry-run and live deployments after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The required API key can manage live crypto trading and create persistent trading deployments with real funds. <br>
Mitigation: Run dry-run deployments and backtests before live use, confirm exact API permissions with Superior Trade, and require explicit user confirmation before any live deployment starts. <br>
Risk: The same API key can close positions and move funds between the user's own Superior Trade or Hyperliquid main and sub-accounts. <br>
Mitigation: Before any transfer, portfolio exit, deployment deletion, or similar operation, show the source, destination, asset, amount, positions, and expected effect, then require explicit confirmation. <br>
Risk: The skill requires sensitive credentials for authenticated API access. <br>
Mitigation: Use only the SUPERIOR_TRADE_API_KEY environment variable or credential manager, do not request private keys or seed phrases, and do not log or display secrets. <br>
Risk: Backtest results and strategy templates may not predict live market performance. <br>
Mitigation: Use fresh backtests, parameter sweeps, and walk-forward checks where appropriate, and present results without implying guaranteed returns. <br>


## Reference(s): <br>
- [Superior Trade account and API key portal](https://account.superior.trade) <br>
- [Superior Trade ClawHub release page](https://clawhub.ai/superior-ai/superiortrade) <br>
- [Superior Trade API endpoint](https://api.superior.trade) <br>
- [Hyperliquid public info endpoint](https://api.hyperliquid.xyz/info) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown guidance with JSON payloads, Python strategy code, configuration examples, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or perform authenticated Superior Trade API operations when SUPERIOR_TRADE_API_KEY is available; live trading, transfers, portfolio exits, and deployment deletion require explicit user confirmation.] <br>

## Skill Version(s): <br>
4.4.6 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
