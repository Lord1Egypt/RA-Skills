## Description:

Browse, search, analyze, and track Wojak Farmers Plot NFTs with floor prices, marketplace listings, rarity estimates, trait information, and local price-history tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[koba42corp](https://clawhub.ai/user/koba42corp)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to answer questions about Wojak Farmers Plot NFTs, compare floor prices and marketplace listings, inspect traits and rarity estimates, and track market history from public NFT data sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts MintGarden, Dexie, and IPFS/Web3.Storage-style URLs for NFT market data.

Mitigation: Install only in environments where those network contacts are acceptable and expected.

Risk: Price-history tracking keeps local JSON market-history files under the skill directory.

Mitigation: Review, retain, or clear those local history files according to the deployment's data retention expectations.

Risk: Wallet credentials or private keys would be inappropriate input for this market lookup skill.

Mitigation: Do not provide wallet credentials, private keys, or other wallet secrets to the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/koba42corp/skills/wojak-ink)
- [Wojak.ink collection website](https://wojak.ink)
- [MintGarden](https://mintgarden.io)
- [Dexie](https://dexie.space)

## Skill Output:

**Output Type(s):** [text, shell commands, code, guidance]

**Output Format:** [Plain text responses suitable for CLI and chat surfaces, with occasional inline command and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public NFT market data and can keep local JSON market-history files when tracking is used.]

## Skill Version(s):

1.0.0 (source: server release metadata, target metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
