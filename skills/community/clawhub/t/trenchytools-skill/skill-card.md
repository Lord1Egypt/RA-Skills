## Description:

Launch and trade memecoins through the TrenchyTools API (pump.fun, PumpSwap, pons on Robinhood Chain). Use when asked to launch a token, bundle-buy at launch, snipe an auto-buy, or give an agent trading with a single API key instead of an RPC node, Jito client and IPFS keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dogtoshi-sz](https://clawhub.ai/user/dogtoshi-sz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare and execute memecoin trades, token launches, bundles, and market monitoring on Solana and Robinhood Chain through the TrenchyTools API. It guides local signing of unsigned transactions and checking their status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A compromised or exposed wallet backup could put funded wallets at risk.

Mitigation: Use a dedicated wallet with limited funds and protect its backup files.

Risk: Signing an unintended transaction can transfer funds or create unwanted fees.

Mitigation: Simulate first, then verify amounts, recipients, and fees before signing; start with small amounts.

Risk: Uploaded token images and metadata may remain publicly accessible.

Mitigation: Treat uploaded images and metadata as public and potentially persistent.

Risk: Live API requirements may have changed since the skill was inspected.

Mitigation: Review the live API instructions before funding a wallet.

## Reference(s):

- [TrenchyTools agent instructions](https://api.trenchy.tools/AGENTS.md)
- [TrenchyTools API specification](https://trenchy.tools/openapi.json)
- [Pump.fun starter (Solana)](https://github.com/Trenchy-Tools/pumpfun-starter)
- [Pons starter (Robinhood Chain)](https://github.com/Trenchy-Tools/pons-starter)
- [Wallet mover starter](https://github.com/Trenchy-Tools/wallet-mover)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with API workflow guidance, shell commands, and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes unsigned transaction workflows that require local signing and status checks.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
