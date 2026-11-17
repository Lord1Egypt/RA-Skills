## Description:

The CoinMarketCap Agent provides agents with access to real-time and historical cryptocurrency market data through CoinMarketCap's official API using the Teneo Protocol SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teneoprotocoldev](https://clawhub.ai/user/teneoprotocoldev)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to query cryptocurrency rankings, quotes, trends, gainers and losers, and performance metrics. It is suited for market research, portfolio monitoring, and trading analysis workflows that can tolerate paid Web3 access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a wallet-capable SDK and automatic USDC payments, and evidence.security reports insufficient in-artifact payment controls.

Mitigation: Use a dedicated low-balance wallet, review the SDK version and wallet setup before installation, require explicit confirmation for every transaction, and avoid primary wallets or broad token allowances.

Risk: The server security verdict is suspicious.

Mitigation: Review the skill and payment behavior before deployment, and install only when the wallet and transaction risks are acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/teneoprotocoldev/skills/teneo-agent-coinmarketcap-agent)
- [Teneo Agent SDK on ClawHub](https://clawhub.ai/teneoprotocoldev/teneo-agent-sdk)
- [Teneo Protocol](https://teneo-protocol.ai)
- [Teneo Protocol SDK on npm](https://www.npmjs.com/package/@teneo-protocol/sdk)
- [CoinMarketCap API v1 Documentation](https://coinmarketcap.com/api/documentation/v1/#section/Introduction)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with TypeScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+, an Ethereum wallet, and USDC on a supported network for paid Teneo Protocol access.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
