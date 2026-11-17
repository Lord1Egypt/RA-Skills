## Description:

A local expense-tracking skill that records spending, queries budgets and reports, analyzes expenses in a snarky tone, aggregates spending by location, and generates trend charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ybl2020](https://clawhub.ai/user/ybl2020)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and agents use this skill to maintain local personal spending records, check budget status, summarize expenses, and generate spending reports or charts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trend chart generation can send spending totals to OpenRouter when an OpenRouter API key is available.

Mitigation: Review or disable scripts/expense_trends.py, or unset OPENROUTER_API_KEY, if external sharing of spending totals is not acceptable; use the local matplotlib fallback instead.

Risk: The skill stores personal spending records on disk.

Mitigation: Set EXPENSE_DATA_FILE to an appropriate protected path and review local file permissions before storing sensitive spending notes.

Risk: The trend script reads OpenClaw auth configuration while looking for OpenRouter profiles.

Mitigation: Review or remove that lookup before deployment if agent auth configuration should not be read.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ybl2020/skills/snarky-expense-butler)
- [OpenRouter Chat Completions API](https://openrouter.ai/api/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands, terminal text output, local JSON data, and optional PNG trend chart files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores expense records in a local JSON file and can write trend charts to a local trends directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
