## Description: <br>
Manage personal finances by recording expenses, income, transfers, checking wallet balances, and generating spending reports through the assistant CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spotsccc](https://clawhub.ai/user/spotsccc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and agents use this skill to maintain a personal finance ledger by creating and querying transactions, wallets, categories, balances, and spending reports. It is suited for user-directed finance tracking where ambiguous transaction details are clarified before changes are made. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change or delete personal finance records through the assistant CLI. <br>
Mitigation: Require explicit approval with a preview of the exact record before delete actions, and keep backups or an undo path for transaction and category changes. <br>
Risk: Incorrect or ambiguous transaction details can create misleading finance records. <br>
Mitigation: Ask one concise clarifying question when required details such as amount, wallet, category, or transfer destination are unclear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/spotsccc/spotsccc-finance) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, JSON, Guidance] <br>
**Output Format:** [Concise text responses with assistant CLI commands and JSON arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses JSON command output from the assistant CLI and replies in the user's language.] <br>

## Skill Version(s): <br>
0.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
