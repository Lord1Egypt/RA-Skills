## Description:

Rebalance an out-of-range Uniswap V3/V4 LP position by closing the old position and opening a new one centered on the current price.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to evaluate and rebalance out-of-range Uniswap V3/V4 liquidity positions, including fee collection, old-position closure, range selection, and re-entry after confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable install commands can change what code is installed over time.

Mitigation: Prefer a pinned release or verified commit before installation.

Risk: Closing and reopening an LP position is irreversible and may realize losses or tax consequences.

Mitigation: Review the chain, pool, position ID, range, gas, slippage, and token approvals before confirming execution.

Risk: A rebalance may be uneconomical when gas costs, slippage, or break-even time outweigh expected fee revenue.

Mitigation: Use the skill's pre-rebalance analysis and proceed only when the cost-benefit estimate is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wpank/skills/rebalance-position)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, API Calls]

**Output Format:** [Markdown-style text with analysis, rebalance plans, confirmation prompts, transaction summaries, and no-action status messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before executing on-chain rebalance actions.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
