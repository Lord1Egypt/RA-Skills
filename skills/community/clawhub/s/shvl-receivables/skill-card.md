## Description:

Read a selected SHVL workspace’s overdue-invoice brief and receivables health to review collection priorities without changing records or sending reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jlucwright](https://clawhub.ai/user/jlucwright)

### License/Terms of Use:

MIT-0

## Use Case:

SHVL workspace members use this skill to review overdue invoices, receivables health and collection priorities without sending reminders or changing records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer and invoice details may be exposed in chat summaries.

Mitigation: Use only an account and workspace the agent is authorized to read, and summarize only the private details needed for the request.

Risk: Installing the published CLI requires trusting SHVL and its package.

Mitigation: Review SHVL and the pinned @shvlapp/cli package before installing.

## Reference(s):

- [SHVL](https://shvl.app)
- [SHVL credit control](https://shvl.app/credit-control)
- [SHVL receivables skill on ClawHub](https://clawhub.ai/jlucwright/skills/shvl-receivables)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the selected workspace, recorded amounts and currency, overdue counts, priorities and available data freshness; does not change records or send reminders.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
