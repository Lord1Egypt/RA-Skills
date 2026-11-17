## Description:

Manage personal finances by recording expenses, income, and transfers, checking balances, and generating spending reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spotsccc](https://clawhub.ai/user/spotsccc)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and assistants use this skill to manage personal finance records through an assistant CLI, including recording transactions, resolving wallets and categories, checking balances, and preparing spending reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify or delete personal finance records, including transactions and categories, through assistant CLI commands.

Mitigation: Require the agent to repeat the exact transaction or category before deletion or other destructive changes, and proceed only after explicit user confirmation.

Risk: Ambiguous wallet, category, amount, or transfer details could lead to an incorrect finance record.

Mitigation: Ask one concise clarifying question whenever required transaction details are missing or unclear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spotsccc/skills/spotsccc-finance)
- [Publisher profile](https://clawhub.ai/user/spotsccc)

## Skill Output:

**Output Type(s):** [Shell commands, Text, JSON]

**Output Format:** [Concise natural-language confirmations with assistant CLI commands and JSON command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create, modify, query, and delete personal finance records through the assistant CLI.]

## Skill Version(s):

0.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
