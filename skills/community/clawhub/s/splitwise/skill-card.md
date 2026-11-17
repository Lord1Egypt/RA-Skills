## Description:

Create and manage expenses on Splitwise when a user wants to log a new expense, split a bill, or check their Splitwise balance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richieforeman](https://clawhub.ai/user/richieforeman)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent create Splitwise expense records, automate two-person 50/50 splits, and optionally attach expenses to groups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create real Splitwise expense records using a long-lived user token.

Mitigation: Require explicit confirmation of payer, participant, amount, group, and description before submitting an expense.

Risk: The long-lived Splitwise token could be exposed through prompts, logs, screenshots, or source files.

Mitigation: Store SPLITWISE_API_KEY only as an environment variable and keep it out of prompts, logs, screenshots, and source files.

Risk: Expense details, user IDs, shares, and group IDs are sent to Splitwise.

Mitigation: Use the skill only when the user accepts sending those expense details to Splitwise.

## Reference(s):

- [Splitwise API Reference](references/api.md)
- [Splitwise Developer Console](https://secure.splitwise.com/apps)
- [Splitwise API v3.0](https://secure.splitwise.com/api/v3.0/)
- [ClawHub Skill Page](https://clawhub.ai/richieforeman/skills/splitwise)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON]

**Output Format:** [Markdown instructions with bash examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SPLITWISE_API_KEY plus Splitwise payer, participant, and optional group IDs.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
