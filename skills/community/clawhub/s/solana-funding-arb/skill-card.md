## Description: <br>
Solana Funding Rate Arbitrage helps agents scan Solana perpetual DEX funding rates, compare Drift and Flash Trade opportunities, simulate and backtest strategies, and configure dry-run or live funding-arbitrage workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zedit42](https://clawhub.ai/user/Zedit42) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and traders use this skill to scan Solana perpetual DEX funding rates, compare cross-exchange spreads, simulate strategies, backtest expected outcomes, and configure dry-run or live funding-arbitrage workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide or run live trading workflows that may use wallet secrets and real funds. <br>
Mitigation: Review the code first, run dry-run mode without wallet secrets, and use a dedicated low-balance wallet only after verifying behavior. <br>
Risk: Advertised yields and delta-neutral claims may not hold under live market conditions, stale data, slippage, or rate reversals. <br>
Mitigation: Independently validate data freshness, spreads, fees, liquidation exposure, and position sizing before enabling automated execution. <br>
Risk: Cron or unattended live trading can repeatedly act on incorrect configuration or market data. <br>
Mitigation: Keep cron and live trading disabled until scan outputs, data sources, risk limits, and alerting have been tested in dry-run mode. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/Zedit42/solana-funding-arb) <br>
- [Publisher Profile](https://clawhub.ai/user/Zedit42) <br>
- [API Reference](references/api.md) <br>
- [Setup Guide](references/setup.md) <br>
- [Strategy Guide](references/strategies.md) <br>
- [Drift Protocol Docs](https://docs.drift.trade) <br>
- [Flash Trade](https://flash.trade) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, TypeScript code paths, JSON configuration examples, CLI output, and dashboard/API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can generate trading scans, dry-run plans, backtest and Monte Carlo summaries, web dashboard data, cron configuration, and live-trading setup guidance when explicitly configured.] <br>

## Skill Version(s): <br>
2.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
