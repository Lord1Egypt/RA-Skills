## Description: <br>
Rebalance an out-of-range Uniswap V3/V4 LP position by closing the old position and opening a new one centered on the current price. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to analyze and rebalance out-of-range Uniswap V3/V4 liquidity positions, including fee collection, cost-benefit review, range selection, and re-entry after confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rebalancing can irreversibly close an existing position, realize impermanent loss, incur gas and slippage, create token approvals, and mint a new LP NFT. <br>
Mitigation: Require explicit user confirmation and verify chain, pool, position ID, token amounts, range, slippage, recipient, deadline, approval limits, and the liquidity-manager subagent before any wallet signature. <br>
Risk: A rebalance may be economically unfavorable when gas costs, position size, or fee expectations do not justify the transaction. <br>
Mitigation: Present pre-rebalance analysis, gas estimates, expected fee revenue, and break-even time, and recommend no action when costs outweigh likely benefits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wpank/rebalance-position) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, API Calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown with transaction summaries, cost estimates, confirmation prompts, and links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include pool data, position identifiers, token amounts, gas estimates, transaction hashes, and no-action recommendations.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
