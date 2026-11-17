## Description:

Extracts completed personal spending events from phone notifications and summarizes totals by category and time period.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vivalavida-say-hi](https://clawhub.ai/user/vivalavida-say-hi)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to analyze local phone notifications for completed payments, refunds, transfers, and spending totals across date ranges or spending categories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local notification files that may include payment, bank, shopping, and transfer details.

Mitigation: Use explicit prompts with a specific date range or category so the agent processes only the notification files needed for the request.

Risk: Spending summaries may include sensitive merchants, amounts, refunds, or personal transfers.

Mitigation: Review the generated summary before sharing it and keep transfer totals separated from consumption spending as the skill directs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vivalavida-say-hi/skills/yoooclaw-expense-tracker)
- [ClawHub publisher profile](https://clawhub.ai/user/vivalavida-say-hi)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown spending summaries with category totals, date breakdowns, transaction notes, and a pending-confirmation section when needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local notification JSON files for the requested date window and separates transfers from spending totals.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
