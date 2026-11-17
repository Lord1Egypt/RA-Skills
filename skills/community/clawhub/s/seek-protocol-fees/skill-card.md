## Description:

Analyzes TokenJar profitability and optionally simulates or executes a Firepit burn-and-claim with preview-only behavior by default.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to check whether Uniswap TokenJar balances justify a Firepit burn, review profitability against UNI burn and gas costs, and optionally proceed through a simulated and confirmed burn-and-claim workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An irreversible 4,000 UNI burn or post-burn swap could proceed from inferred wording without transaction-specific confirmation.

Mitigation: Require fresh human approval for every burn and swap, confirming chain, contract, amount, recipient, selected assets, gas limit, and expected proceeds before execution.

Risk: Profitability can change before broadcast because gas prices, TokenJar balances, or Firepit nonce may change.

Mitigation: Re-check gas, TokenJar state, and Firepit nonce immediately before execution, and abort on nonce changes, failed simulation, safety rejection, or marginal profitability.

## Reference(s):

- [Skill specification](artifact/SKILL.md)
- [README](artifact/README.md)
- [ClawHub skill page](https://clawhub.ai/wpank/skills/seek-protocol-fees)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style profitability reports and execution status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include per-asset value breakdowns, burn cost, gas estimate, net profit, ROI, verdict, confirmation prompts, transaction status, and post-burn conversion details.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
