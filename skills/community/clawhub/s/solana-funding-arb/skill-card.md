## Description:

Solana perpetual DEX funding rate arbitrage scanner and auto-trader that compares funding rates across Drift and Flash Trade to find cross-DEX opportunities, with simulation and backtesting support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zedit42](https://clawhub.ai/user/zedit42)

### License/Terms of Use:

MIT

## Use Case:

External developers and traders use this skill to scan Solana perpetual DEX funding rates, review delta-neutral funding arbitrage opportunities, run simulations or backtests, and configure dry-run or live auto-trading workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live auto-trading safeguards are weak enough that users should review the skill carefully before installing or running it.

Mitigation: Audit and modify the trading code before live use, keep dry_run enabled while testing, and begin with minimal position limits only after review.

Risk: Raw private keys may be stored in or loaded from a sourced shell environment file for wallet initialization.

Mitigation: Avoid storing raw private keys in sourced shell files; prefer a secured wallet file or hardened secret management with restricted local permissions.

Risk: Cron execution can repeatedly run the auto-trader with environment variables loaded from user secrets.

Mitigation: Do not add the cron job until environment loading is hardened and dry-run behavior, logging, and failure handling are verified.

Risk: A failed second trading leg can leave an unmatched first leg because rollback is not complete.

Mitigation: Require complete two-leg execution handling with rollback or fail-closed behavior before enabling live trading.

Risk: Bad or fallback market data can influence automated trading decisions.

Mitigation: Validate live market data sources and require the trader to fail closed when fresh, trustworthy data is unavailable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zedit42/skills/solana-funding-arb)
- [API Reference](references/api.md)
- [Setup Guide](references/setup.md)
- [Strategy Guide](references/strategies.md)
- [Drift Protocol Docs](https://docs.drift.trade)
- [Flash Trade](https://flash.trade)
- [CoinGecko Derivatives API](https://api.coingecko.com/api/v3/derivatives)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CLI output summaries, dashboard setup guidance, dry-run trading instructions, and references to local state or configuration files.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
