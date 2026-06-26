## Description: <br>
Submit a UniswapX Dutch auction limit order for a token pair with optional chain, limit price, expiry, status monitoring, and MEV-protected execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to prepare and submit UniswapX limit orders with token, amount, chain, price, and expiry details. It is intended for workflows where the user wants a target price, no upfront gas cost, and order status feedback after submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit real crypto trades and may not require a clear final confirmation before order submission. <br>
Mitigation: Require the agent to display the exact wallet, chain, token pair, amount, limit or minimum received, expiry, and cancellation or fill implications, then obtain explicit user approval before submitting an order. <br>
Risk: A compromised or untrusted Uniswap MCP, wallet connection, or trade-executor setup could affect order submission or reporting. <br>
Mitigation: Use the skill only with trusted wallet, Uniswap MCP, and trade-executor configurations, and review the proposed order details before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wpank/submit-limit-order) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown status summaries with order details, order status, and error guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include wallet, chain, token pair, amount, limit or minimum received, expiry, monitoring status, and order hash.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
