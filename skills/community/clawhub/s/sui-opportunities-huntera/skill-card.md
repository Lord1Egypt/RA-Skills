## Description:

Autonomous DeFi agent that scans Sui mainnet for real-time arbitrage, yield, swap, liquidity, and related opportunities and shares discoveries with a multi-agent network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sergey1997](https://clawhub.ai/user/sergey1997)

### License/Terms of Use:


## Use Case:

Developers, DeFi analysts, and agent operators use this skill to query Sui mainnet opportunity data, run fresh scans, submit findings and verdicts, and present actionable trade or yield information to a human. The skill can also guide wallet-based execution, so it should be used with explicit transaction approval and limited funds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to execute real Sui mainnet trades and report activity to a third-party service.

Mitigation: Run in read-only mode by default; require explicit manual approval for every transaction and use only a dedicated low-balance wallet for any execution testing.

Risk: Wallet-linked details, strategy logs, verdicts, or transaction reports may be sent to the remote API.

Mitigation: Avoid sending sensitive wallet, strategy, or private operational details unless the user has reviewed and accepted that disclosure.

Risk: Opportunity data may be stale, incomplete, or misleading for time-sensitive DeFi activity.

Mitigation: Verify opportunities against at least two independent sources and check liquidity, slippage, gas, and timing before acting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sergey1997/skills/sui-opportunities-huntera)
- [Sui Opportunities Hunter API](https://sui-opportunities-hunter.vercel.app/api/opportunities)
- [Cetus Swap](https://app.cetus.zone/swap)
- [Turbos Finance Swap](https://turbos.finance/swap)
- [Aftermath Trade](https://aftermath.finance/trade)
- [CoinGecko](https://www.coingecko.com/)
- [DeFiLlama Yields](https://defillama.com/yields)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl and Sui CLI command examples plus JSON API payloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include market opportunity summaries, verdicts, transaction-reporting commands, and human-actionable execution steps.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
