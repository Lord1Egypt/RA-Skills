## Description:

MCP Server for Web3 Daily - Real-time Web3 research digest with macro news, KOL sentiment, market data, and personalized wallet analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexander10011](https://clawhub.ai/user/alexander10011)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can connect this MCP server to an MCP-compatible agent to retrieve Web3 daily digests, crypto market summaries, and wallet-based analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personalized tools send wallet addresses selected by the user to the J4Y backend for analysis.

Mitigation: Use personalized wallet-analysis features only with wallet addresses users are comfortable submitting to the disclosed backend.

Risk: Unversioned npx installation examples can fetch a newer package than the reviewed release.

Mitigation: Prefer a pinned package version or a local build when deploying this MCP server.

Risk: The server depends on live backend and market-data availability, so outputs may fail or change with upstream service state.

Mitigation: Treat returned market and wallet analysis as live external data and handle MCP tool errors in the calling agent workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexander10011/skills/web3-daily-mcp)
- [J4Y Backend API](https://j4y-production.up.railway.app)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Text or Markdown returned through MCP tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Chinese and English output for digest and wallet-analysis tools.]

## Skill Version(s):

1.0.0 (source: package.json, claw.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
