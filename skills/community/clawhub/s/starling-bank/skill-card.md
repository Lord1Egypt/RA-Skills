## Description:

Manage Starling Bank accounts through the starling-bank-mcp server, including balances, transactions, payees, payments, savings goals, cards, direct debits, and standing orders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gpunter](https://clawhub.ai/user/gpunter)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to operate a Starling Bank account through MCP workflows for account lookup, transaction review, payee management, payments, savings goal transfers, direct debits, standing orders, and card status changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive banking data and account identifiers.

Mitigation: Use the narrowest Starling token scopes, store the token in a protected secret store, and require confirmation before displaying sensitive account details.

Risk: The skill can initiate money-moving or account-changing actions, including payments, payee changes, savings transfers, and card changes.

Mitigation: Require explicit human confirmation before every payment, payee change, savings transfer, card change, or similarly sensitive operation.

Risk: Server-resolved source provenance is unavailable for this version.

Mitigation: Review the MCP package source and provenance before installation and pin a trusted package version.

## Reference(s):

- [Starling Bank API Details](references/api-details.md)
- [Starling Developer Portal](https://developer.starlingbank.com/)
- [ClawHub Skill Page](https://clawhub.ai/gpunter/skills/starling-bank)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and MCP call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured starling-bank-mcp server, mcporter, and a Starling personal access token; monetary amounts use minor units.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
