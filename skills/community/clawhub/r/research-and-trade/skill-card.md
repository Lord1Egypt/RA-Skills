## Description: <br>
Research a token and execute a trade if it passes due diligence; the pipeline researches the token, evaluates pool and trade risk, asks for confirmation, and stops with a report if risk is too high. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to run an autonomous Uniswap research-to-trade workflow: investigate a token, select a pool, assess risk, and execute only after due diligence and explicit user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill coordinates crypto trades and may have high-impact trading authority if connected to a wallet. <br>
Mitigation: Before use, verify the referenced subagents and Uniswap tools, confirm exactly which wallet the agent can access, and set strict spend and approval limits. <br>
Risk: Trade execution can expose users to loss from poor liquidity, slippage, unsafe tokens, or incorrect risk assessment. <br>
Mitigation: Review each research, pool, and risk report, require explicit confirmation, and manually inspect every final transaction before signing. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/wpank/research-and-trade) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown progress updates and final trade, veto, or error report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided trade amount and explicit user confirmation before execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
