## Description:

Swap or trade tokens on the Base network between assets such as USDC, ETH, and WETH.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xrag](https://clawhub.ai/user/0xrag)

### License/Terms of Use:


## Use Case:

External users use this skill to direct an agent to check wallet status and swap, buy, sell, or convert supported tokens on the Base network after authentication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent real authority to submit crypto token trades.

Mitigation: Use a wallet with limited funds and permissions, and require manual confirmation showing exact trade details before any transaction is submitted.

Risk: The skill invokes an unpinned npm command for the trading CLI.

Mitigation: Use a pinned and trusted version of the trading CLI before enabling the skill.

Risk: Trades may fail or execute incorrectly when token addresses, balances, slippage, approvals, or liquidity are unsuitable.

Mitigation: Confirm wallet status, token pair, amount, slippage, balance, and expected trade details before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xrag/skills/trade)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON]

**Output Format:** [Markdown guidance with inline bash commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authenticated wallet, sufficient source-token balance, supported token aliases or contract addresses, and optional slippage settings.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
