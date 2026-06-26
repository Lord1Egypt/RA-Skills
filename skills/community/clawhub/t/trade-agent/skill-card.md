## Description: <br>
AIUSD trading and account management skill. Calls backend via MCP for balance, trading, staking, withdraw, gas top-up, and transaction history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChaunceyLiu](https://clawhub.ai/user/ChaunceyLiu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to manage AIUSD accounts through an agent, including checking balances, executing trades, staking or unstaking, withdrawing funds, topping up gas, and reviewing transaction history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate real financial actions, including trades, staking, withdrawals, and gas top-ups. <br>
Mitigation: Review every asset, amount, chain, and destination before execution, use small transaction limits, and require explicit user confirmation for fund-moving actions. <br>
Risk: The installer can remove a prior local install directory and run npm dependency scripts during setup. <br>
Mitigation: Inspect the unpacked package before installation and run setup in an isolated environment until the installer behavior is trusted. <br>
Risk: The skill handles local authentication tokens. <br>
Mitigation: Limit token access to the intended local user account and rotate or clear tokens if the environment is shared or compromised. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ChaunceyLiu/trade-agent) <br>
- [AIUSD website](https://aiusd.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown and plain text with inline shell commands and tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initiate account, trading, staking, withdrawal, gas top-up, and transaction-history actions through MCP-backed AIUSD tools after authentication.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
