## Description:

Trade Solana tokens, track portfolio, bet on prediction markets, check NFT floors via the trader CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devatzeroxcore](https://clawhub.ai/user/devatzeroxcore)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to direct an agent through Solana wallet diagnostics, token swaps, portfolio checks, prediction-market positions, perpetual-market views, and NFT floor lookups through the trader CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate a real-money trading wallet and sign transactions.

Mitigation: Use a dedicated low-value wallet, scope credentials carefully, and require manual approval for swaps, prediction-market trades, --force actions, and private-key export.

Risk: The install path uses an external CLI package that may be run through a floating npx invocation.

Mitigation: Use only a pinned, reviewed version of the trader CLI and prefer provenance or integrity verification before using a wallet with funds.

Risk: The artifact includes VPN guidance for blocked prediction markets.

Mitigation: Do not use VPNs to bypass jurisdiction or platform restrictions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/devatzeroxcore/skills/zeroexcore-trader)
- [trader CLI homepage](https://github.com/zeroexcore/trader)
- [Helius API keys](https://dev.helius.xyz)
- [Jupiter API keys](https://portal.jup.ag)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI output that may be JSON or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the trader binary plus WALLET_PASSWORD and HELIUS_API_KEY; swaps and prediction-market trades may also require JUPITER_API_KEY.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
