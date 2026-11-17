## Description:

Binance Spot request using the Binance API. Authentication requires API key and secret key. Supports testnet and mainnet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[awessh](https://clawhub.ai/user/awessh)

### License/Terms of Use:

MIT

## Use Case:

Developers and trading operators use this skill to have an agent prepare Binance Spot API requests, including market data queries and authenticated account or order operations against testnet or mainnet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live account-changing operations can place, cancel, or amend Binance Spot orders when mainnet credentials are used.

Mitigation: Use testnet for development, require explicit confirmation for every live account-changing request, and keep live API keys tightly scoped.

Risk: High-value Binance API keys or secret keys can be exposed if stored in repository files, TOOLS.md, or chat-visible content.

Mitigation: Use a secure secret store, avoid writing credentials to shared files or chats, apply IP allowlisting, and disable withdrawal permission.

## Reference(s):

- [Binance Authentication](artifact/references/authentication.md)
- [Binance Spot Skill](https://clawhub.ai/awessh/skills/spot)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Binance API credentials for authenticated endpoints; supports testnet and mainnet.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
