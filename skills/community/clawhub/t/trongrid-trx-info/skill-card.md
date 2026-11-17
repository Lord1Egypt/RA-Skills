## Description:

Query TRX token fundamentals including price, supply, burn rate, market cap, staking yield, and network economics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[greason](https://clawhub.ai/user/greason)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for TRX price, supply, burn-rate, staking-yield, and network-economics reports using TronGrid data and public market sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Current blockchain or market data may be unavailable, stale, or rate-limited.

Mitigation: Report available on-chain data, clearly state when market data is unavailable, and label time-sensitive values as current only at retrieval time.

Risk: Burn-rate and staking-yield calculations are approximate and depend on sampled blocks, witness rewards, brokerage, and public market sources.

Mitigation: Show calculation assumptions and present estimates as approximate rather than guaranteed values.

## Reference(s):

- [TronGrid MCP Guide](https://developers.tron.network/reference/mcp-api)
- [ClawHub skill page](https://clawhub.ai/greason/skills/trongrid-trx-info)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown analysis report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include current on-chain metrics, public market data, calculations, and caveats about unavailable or approximate data.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
