## Description: <br>
Manage Starling Bank accounts via the starling-bank-mcp server, including balances, transactions, payees, payments, savings goals, direct debits, standing orders, and cards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Gpunter](https://clawhub.ai/user/Gpunter) <br>

### License/Terms of Use: <br>


## Use Case: <br>
People using Starling Bank and their agents use this skill to query account information and initiate supported banking actions through the Starling MCP server. It is intended for workflows involving balances, transactions, payments, savings goals, direct debits, standing orders, and card controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent access to real Starling banking data and write or payment scopes on the token. <br>
Mitigation: Use read-only or minimum required token scopes, verify and pin the MCP package, and keep the token out of persistent memory or shared configuration. <br>
Risk: Payment, payee, card, transaction-edit, and savings actions can affect real accounts. <br>
Mitigation: Require explicit human confirmation before every money movement, payee change, card control, transaction edit, or savings action. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Gpunter/starling-bank) <br>
- [Starling Bank Developer Portal](https://developer.starlingbank.com/) <br>
- [Starling Bank API Details](references/api-details.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the starling-bank-mcp npm package and a Starling personal access token.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
