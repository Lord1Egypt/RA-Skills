## Description:

Create and manage XRPL issued tokens and NFTs, including minting, trust lines, issuing payments, and setting NFT offers with customizable fees and flags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harleyscodes](https://clawhub.ai/user/harleyscodes)

### License/Terms of Use:


## Use Case:

Developers and blockchain builders use this skill to draft XRPL issued-currency and NFT transaction templates for minting, trust lines, payments, and NFT offers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live XRPL transaction templates can affect assets irreversibly if used on mainnet without review.

Mitigation: Use testnet or devnet until the network, wallet, account ownership, issuer and destination addresses, amounts, fees, flags, and consequences of each transaction are explicitly confirmed.

Risk: Dependency behavior may change if the xrpl package version is left floating.

Mitigation: Pin and review the xrpl package version before adapting the templates in real projects.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harleyscodes/skills/xrpl-token-mint)
- [Publisher profile](https://clawhub.ai/user/harleyscodes)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands and TypeScript-like XRPL transaction snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides transaction templates and implementation guidance; it does not execute XRPL transactions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
