## Description: <br>
XT.COM exchange CLI for spot and futures trading workflows, including market data, balances, orders, transfers, and withdrawals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realm520](https://clawhub.ai/user/realm520) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent retrieve XT.COM spot and futures market data and prepare account, order, transfer, and withdrawal commands. Authenticated account operations require XT.COM API credentials and user review before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables live financial actions such as trades, transfers, cancellations, and withdrawals through an agent. <br>
Mitigation: Require explicit user confirmation for every trade, transfer, cancellation, or withdrawal, and review full action parameters before execution. <br>
Risk: The skill requires powerful XT.COM API credentials that could expose account access if mishandled. <br>
Mitigation: Use least-privilege API keys, disable withdrawals unless needed, avoid plaintext credential storage, and prevent the agent from printing or displaying secrets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/realm520/xt-exchange) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and tabular command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses python3 scripts and XT_ACCESS_KEY and XT_SECRET_KEY for authenticated XT.COM account operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
