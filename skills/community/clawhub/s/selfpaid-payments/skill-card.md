## Description:

Helps AI agents create Base USDC payment batches, inspect treasury and yield data, and prepare collateral withdrawals through Aave V3 or Morpho.

This skill is ready for commercial/non-commercial use.

## Publisher:

[altoninelli](https://clawhub.ai/user/altoninelli)

### License/Terms of Use:

MIT

## Use Case:

AI agent developers and smart account users can use the skill to request USDC payment quotes, build unsigned Base transaction batches, track treasury balances, and prepare collateral withdrawals. Users should inspect transaction details and recovery assumptions before signing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that payment validation accepts excessive collateral deposits.

Mitigation: Keep automatic signing disabled until collateral limits are independently enforced, and verify decoded transaction amounts and total spending before signing.

Risk: Advertised recovery times conflict with the skill’s formula, and recovery estimates depend on yield assumptions.

Mitigation: Treat recovery estimates as uncertain and independently review the quote, fee minimum, and total upfront amount.

Risk: The hosted operator receives payment details.

Mitigation: Review the wallet and payment information sent to the hosted service before using it.

Risk: The optional MCP installation should be tied to a reviewed release.

Mitigation: Pin any optional MCP installation to a release that has been reviewed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/altoninelli/skills/selfpaid-payments)
- [SelfPaidPal service and dashboard](https://selfpaid.cryptofolio.it)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON transaction payloads and Markdown integration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Per-request payment and treasury data, unsigned transaction calls, and recovery estimates.]

## Skill Version(s):

2.1.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
