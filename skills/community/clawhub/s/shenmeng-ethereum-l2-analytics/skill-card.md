## Description:

Ethereum L2 Analytics analyzes Ethereum Layer 2 protocols such as Optimism, Arbitrum, Base, zkSync, and Starknet for ecosystem trends, TVL monitoring, technical comparison, bridge analysis, and investment-opportunity discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenmeng](https://clawhub.ai/user/shenmeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze Ethereum L2 ecosystems, compare rollup projects, evaluate bridges, monitor L2 fund-flow narratives, and identify potential market or airdrop opportunities. Outputs should be treated as informational because server security evidence flags static data and payment-verification concerns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid verification and wallet-address handling may not be clear to the user.

Mitigation: Confirm payment terms before use and do not provide a wallet address unless transmission to SkillPay is acceptable.

Risk: An exposed payment API key is present in the artifact metadata.

Mitigation: Rotate or remove the exposed key and require deployment-time secrets before publishing or installing.

Risk: Static or stale L2 data could lead to misleading investment or bridge recommendations.

Mitigation: Verify outputs against current trusted sources and treat financial or bridge guidance as informational, not financial advice.

## Reference(s):

- [Ethereum L2 protocol database](references/l2-protocols.md)
- [Ethereum L2 bridge guide](references/bridge-guide.md)
- [DefiLlama API](https://api.llama.fi)
- [L2Beat API](https://l2beat.com/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with analysis summaries and optional Python or shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include market-monitoring guidance, project scoring, bridge comparisons, and payment-verification considerations.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
