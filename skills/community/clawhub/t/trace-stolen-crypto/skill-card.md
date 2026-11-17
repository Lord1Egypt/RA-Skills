## Description:

Use when the user wants to trace where crypto funds went, investigate a wallet address or transaction hash, or check whether an address is risky (stolen funds, scams, hacks). Calls the MistTrack on-chain investigation agent by SlowMist through Finch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a0971025732-netizen](https://clawhub.ai/user/a0971025732-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

External users can provide a wallet address or transaction hash to investigate fund flows, transaction relationships, and potential address risks. The tracing service does not recover funds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet addresses or transaction hashes, along with the user's interest in them, are shared with Finch and MistTrack for analysis.

Mitigation: Proceed only if comfortable sharing this information with those services. Never provide a seed phrase or private key.

Risk: Paid tracing runs cost 0.5 USDC per run.

Mitigation: Use free runs only unless the user explicitly approves a paid run, and confirm free-run availability before proceeding.

Risk: Tracing results do not recover stolen funds.

Mitigation: Do not present tracing as recovery; warn users not to pay anyone promising fund recovery.

## Reference(s):

- [MistTrack agent on Finch](https://www.finchtech.ai/market/chips/agent-3dcaa57f-b8b8-5c78-9300-c972e5a764bc/run?utm_source=skill&utm_medium=agent&utm_campaign=toa_skills&utm_content=trace-stolen-crypto)
- [Finch MCP server](https://www.finchtech.ai/mcp)
- [Finch agent connection guide](https://github.com/a0971025732-netizen/finch-agents/blob/main/CONNECT.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [On-chain investigation findings for a wallet address or transaction hash; tracing does not recover funds.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
