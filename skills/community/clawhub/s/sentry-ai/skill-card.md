## Description:

Solana/Base Multi-Chain Meme Scanner & Auditor (Anti-Rug)

This skill is for research and development only.

## Publisher:

[qiyun154-cyber](https://clawhub.ai/user/qiyun154-cyber)

### License/Terms of Use:


## Use Case:

External developers and crypto-market analysts can use this skill to scan Solana and Base token-pool data and generate basic token risk reports. Its outputs should be treated as research signals, not trading recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may overstate crypto audit and token safety capabilities and may label tokens as safe using weak checks.

Mitigation: Treat outputs as market-data hints only and require independent contract, liquidity, holder-distribution, and trading-risk review before acting.

Risk: The artifact describes execution features such as take-profit, stop-loss, and gas optimization in a financial context.

Mitigation: Do not connect wallets or automate trades based on this package without separate security checks, manual approval, and appropriate operational controls.

Risk: The audit script can report UNKNOWN for liquidity and holder distribution while still producing a recommendation.

Mitigation: Require complete external data and clearly treat UNKNOWN checks as unresolved risk rather than evidence of token safety.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qiyun154-cyber/skills/sentry-ai)
- [DexScreener Solana token endpoint](https://api.dexscreener.com/latest/dex/tokens/solana)
- [DexScreener Base token endpoint](https://api.dexscreener.com/latest/dex/tokens/base)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text terminal output with token metadata, risk scores, audit checks, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May depend on external DEX data availability; audit checks are basic and may return UNKNOWN for liquidity and holder distribution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
