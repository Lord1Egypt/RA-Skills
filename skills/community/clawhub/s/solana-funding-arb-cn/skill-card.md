## Description: <br>
Monitors Solana perpetual DEX funding rates, compares cross-exchange spreads, and helps identify or run funding-rate arbitrage workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guohongbin-git](https://clawhub.ai/user/guohongbin-git) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to scan Solana perpetual DEX funding rates, compare arbitrage spreads, and configure dry-run or live trading workflows. It is intended for users who understand crypto trading, wallet custody, and automated execution risk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet keys, live mode, and cron execution can enable automated fund movement. <br>
Mitigation: Use dry-run mode first, do not provide wallet or private key material unless you accept live trading risk, and avoid cron/live mode until the code and configuration are reviewed. <br>
Risk: Trading decisions may rely on unsafe mock or fallback data. <br>
Mitigation: Confirm live market data sources and rate freshness before executing trades or increasing position size. <br>
Risk: Advertised returns and Ultra Safe wording may be read as guarantees. <br>
Mitigation: Treat return estimates as hypothetical, verify assumptions independently, and size positions conservatively. <br>


## Reference(s): <br>
- [API Reference](references/api.md) <br>
- [Setup Guide](references/setup.md) <br>
- [Strategy Guide](references/strategies.md) <br>
- [Drift Protocol Docs](https://docs.drift.trade) <br>
- [Flash Trade](https://flash.trade) <br>
- [ClawHub Skill Page](https://clawhub.ai/guohongbin-git/solana-funding-arb-cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, TypeScript code references, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate command plans for scanning, dashboard use, dry runs, live trading, and cron setup.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
