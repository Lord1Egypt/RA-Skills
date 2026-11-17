## Description:

Guides autonomous agents through checking credit, requesting USDC loans, and repaying them on Base mainnet using a Coinbase CDP wallet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rsoft-latam](https://clawhub.ai/user/rsoft-latam)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators of autonomous agents use this skill to check credit, request real USDC loans, manage human sponsorship, and repay loans through a Coinbase CDP wallet on Base mainnet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled one-step repayment helper can transfer real USDC using a recipient and amount supplied by the bank without final local confirmation or a spending limit.

Mitigation: Avoid the one-step helper unless the recipient and amount have been independently verified; prefer the documented three-step repayment flow with human review before transfer.

Risk: CDP credentials can control every wallet in their project, exposing other funds if reused or disclosed.

Mitigation: Use a dedicated low-balance CDP project and wallet, and keep the wallet configuration file private.

Risk: Loan requests and transfers involve real USDC on Base mainnet and can create financial losses.

Mitigation: Require human review before requesting loans or transferring USDC.

## Reference(s):

- [RSoft Agentic Bank documentation](https://rsoft-agentic-bank.com/docs)
- [RSoft Agentic Bank website](https://rsoft-agentic-bank.com/)
- [ClawHub skill release](https://clawhub.ai/rsoft-latam/skills/rsoft-agentic-bank)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Coinbase CDP wallet and credentials; loan requests also require a bank API key.]

## Skill Version(s):

2.5.0 (source: skill frontmatter, package.json, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
