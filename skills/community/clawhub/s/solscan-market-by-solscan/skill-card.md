## Description:

Use this skill to query Solana blockchain data through the Solscan Pro API for accounts, tokens, NFTs, transactions, blocks, DeFi activity, markets, programs, and API usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tiennv3](https://clawhub.ai/user/tiennv3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to inspect Solana wallets, tokens, NFTs, transactions, DeFi activity, markets, blocks, and programs through Solscan Pro. It supports targeted blockchain lookups, token and NFT analysis, transaction review, and API usage checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet addresses, token identifiers, filters, and the Solscan API key are sent to Solscan Pro for lookups.

Mitigation: Use the skill only for legitimate wallet or token investigations, avoid unnecessary sensitive lookups, and protect the SOLSCAN_API_KEY value.

Risk: Some documented commands may be inaccurate, unsupported, or affected by Solscan API changes.

Mitigation: Validate important results against Solscan Pro documentation or direct API responses, and handle API errors before relying on the output.

Risk: Export and lookup requests can be constrained by Solscan API limits or authentication failures.

Mitigation: Check API key status, respect documented rate limits, and retry only with appropriate backoff.

## Reference(s):

- [Solscan Pro API Docs](https://pro-api.solscan.io/pro-api-docs/v2.0)
- [Solscan Pro API FAQs](https://pro-api.solscan.io/pro-api-docs/v2.0/faq.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SOLSCAN_API_KEY and sends read-only lookup requests to Solscan Pro.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
