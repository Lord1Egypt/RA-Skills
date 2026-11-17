## Description:

Retrieves Chinese stock and sector quotes, historical prices, and financial data through multiple public market-data providers with automatic fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clementgu](https://clawhub.ai/user/clementgu)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to look up Chinese stock and index prices, historical candles, sector rankings and constituents, and financial data. Additional commands cover ETFs, futures, and market breadth.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market-data queries send requested symbols and network metadata to external finance providers.

Mitigation: Use only where outbound requests to those providers are acceptable; avoid querying sensitive holdings or watchlists.

Risk: Additional finance commands are not fully described in the skill overview.

Mitigation: Review the script help before enabling or relying on those commands.

Risk: Provider data can be delayed, unavailable, or subject to request limits.

Mitigation: Check timestamps and corroborate important figures with an authoritative market source before acting.

## Reference(s):

- [ClawHub stock-unified release](https://clawhub.ai/clementgu/skills/stock-unified)
- [Data source reference](references/data_sources.md)
- [Eastmoney market-data endpoint](https://datacenter.eastmoney.com/api/data/v1/get)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Plain text tables or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Market-data results depend on provider availability and may be delayed.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
