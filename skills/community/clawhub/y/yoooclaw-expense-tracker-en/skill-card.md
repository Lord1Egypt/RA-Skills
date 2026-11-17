## Description:

Extract personal consumption transactions from mobile phone notifications, summarize them by category and time, and provide total spending.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vivalavida-say-hi](https://clawhub.ai/user/vivalavida-say-hi)

### License/Terms of Use:

MIT-0

## Use Case:

Individual users use this skill to summarize personal spending from mobile notifications over requested time windows and categories. It helps separate consumption, transfers, refunds, and uncertain entries for expense review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads sensitive mobile notification data, including payment, bank, shopping, delivery, taxi, and transfer notifications.

Mitigation: Use the skill only when this access is acceptable, and request narrow date ranges and categories whenever possible.

Risk: Expense totals can be misleading if duplicate notifications or unclear amount fields are not handled correctly.

Mitigation: Review detailed entries, transfers, refunds, and the to-be-confirmed section before relying on totals for decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vivalavida-say-hi/skills/yoooclaw-expense-tracker-en)
- [ClawHub publisher profile](https://clawhub.ai/user/vivalavida-say-hi)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown expense summary with category and date breakdowns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports totals, transaction counts, transfers separated from consumption, refunds as negative amounts, and uncertain items when needed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
