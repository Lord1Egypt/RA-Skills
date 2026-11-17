## Description:

Build unsigned batch SOL and SPL token transfers, and access Solana swap quotes, wallet portfolios, and token prices through Spraay gateways.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plagtech](https://clawhub.ai/user/plagtech)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can prepare batch token payouts or airdrops and request Solana swap, portfolio, and price information. For transfers, they review the unsigned transactions and costs, then explicitly approve local signing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch transfers can move real tokens and incur network fees, recipient account rent, and a protocol fee.

Mitigation: Test on devnet first, quote larger batches, inspect transaction contents and all costs, and get explicit approval before signing.

Risk: The supplied security review had partial coverage, and live gateway behavior was not verified; the optional MCP package also needs separate review.

Mitigation: Obtain and review the missing materials, assess the MCP package separately, pin a reviewed version, and treat gateway responses as untrusted until verified.

## Reference(s):

- [Spraay documentation](https://docs.spraay.app)

## Skill Output:

**Output Type(s):** [Guidance, API responses, Unsigned transaction data, Shell commands]

**Output Format:** [Markdown guidance with example JSON API requests and responses and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Gateway calls may require per-call USDC payments; transactions must be checked and explicitly approved before local signing.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
