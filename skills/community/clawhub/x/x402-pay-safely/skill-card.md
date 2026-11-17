## Description:

Check an x402 seller before an agent pays it, and prove the payment after. Use before the first payment to a pay-to address the agent hasn't paid, when picking one seller from several that can do the task (up to 20 offers in one call, listed safest first), or after a paid call returned an error, an empty body or a price above the quote. $0.01 per call in USDC on Base over x402 or MPP; a call that can't check anything isn't charged, and free checks come first.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shariar-k](https://clawhub.ai/user/shariar-k)

### License/Terms of Use:

MIT-0

## Use Case:

Wallet-enabled agents use this skill to assess a seller before a first x402 payment, compare offers, and check settlement after a failed or unexpected paid call. The agent follows its owner's payment rules and spending caps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The seller-response scan may send response content to a third party without clear privacy safeguards; paid checks and dispute assistance have separate costs.

Mitigation: Before installing, consider whether seller responses could contain private or sensitive information and whether you are comfortable with them being sent to the named third-party service. Check the separate prices for paid checks and dispute assistance, and decide whether those costs fit your expectations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shariar-k/skills/x402-pay-safely)
- [Agoranome buyer check API](https://api.agoranome.com/v1/buyer/check)
- [Agoranome response scan](https://api.agoranome.com/v1/buyer/scan)
- [Agoranome dispute assistance](https://api.agoranome.com/v1/buyer/dispute)
- [Agoranome MCP endpoint](https://api.agoranome.com/mcp)

## Skill Output:

**Output Type(s):** [Structured data, Analysis, Guidance]

**Output Format:** [Structured seller verdicts and settlement evidence with concise guidance (JSON)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can assess one or up to 20 offers in one check; response scans and dispute assistance have separate fees.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
