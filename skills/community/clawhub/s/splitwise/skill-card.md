## Description: <br>
Create and manage expenses on Splitwise. Use this skill when the user wants to log a new expense, split a bill, or check their Splitwise balance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richieforeman](https://clawhub.ai/user/richieforeman) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent create 50/50 Splitwise expenses, split bills, and record shared costs through the Splitwise API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create real Splitwise expense records using a long-lived account token. <br>
Mitigation: Keep SPLITWISE_API_KEY in a secure environment variable or secret manager, rotate it if exposed, and require confirmation of amount, payer, participant, group, and shares before submitting an expense. <br>
Risk: Expense amounts, descriptions, user IDs, shares, group IDs, and the Splitwise token are sent to Splitwise when creating expenses. <br>
Mitigation: Install only if sharing this data with Splitwise is acceptable, and review expense details before the agent sends the API request. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/richieforeman/splitwise) <br>
- [Splitwise API Reference](references/api.md) <br>
- [Splitwise Developer Console](https://secure.splitwise.com/apps) <br>
- [Splitwise Create Expense Endpoint](https://secure.splitwise.com/api/v3.0/create_expense) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SPLITWISE_API_KEY and user-supplied Splitwise user or group identifiers.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
