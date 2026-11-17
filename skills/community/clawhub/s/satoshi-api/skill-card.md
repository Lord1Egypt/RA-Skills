## Description:

Bitcoin intelligence: fee recommendations, mempool status, price, block info, and address lookups via the Satoshi API. Zero config — no node required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bortlesboat](https://clawhub.ai/user/bortlesboat)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users use this skill to query Bitcoin fees, mempool status, price, recent block data, address information, and halving estimates without running a Bitcoin node or configuring an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bitcoin queries, especially address lookups, are sent to bitcoinsapi.com.

Mitigation: Avoid querying addresses tied to a user identity when privacy is important, or use an alternative version configured for a trusted node or API source.

Risk: The Python script declares an unpinned httpx dependency.

Mitigation: Review dependency resolution before deployment and pin approved package versions in managed environments.

Risk: Results depend on live third-party API availability and current network data.

Mitigation: Treat responses as point-in-time data and retry or cross-check critical fee, price, and address decisions against an independent source.

## Reference(s):

- [Satoshi API](https://bitcoinsapi.com)
- [Satoshi API v1 endpoint](https://bitcoinsapi.com/api/v1)
- [bitcoin-mcp related MCP server](https://github.com/Bortlesboat/bitcoin-mcp)
- [ClawHub skill page](https://clawhub.ai/bortlesboat/skills/satoshi-api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown-style text with command-line examples and API-derived Bitcoin data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API key is required; live responses depend on bitcoinsapi.com availability and current Bitcoin network data.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
