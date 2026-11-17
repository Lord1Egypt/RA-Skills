## Description:

SaaS and subscription business revenue intelligence for tracking MRR, ARR, churn, net revenue retention, lifetime value, cohort retention, payback periods, investor reporting, and deferred revenue journal entry preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Finance operators, founders, and developers use this skill to calculate SaaS subscription metrics from Stripe, Chargebee, or CSV exports and prepare investor-facing summaries or deferred revenue schedules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples show live Stripe secret key placeholders in shell and Python snippets, which could encourage unsafe credential handling if copied directly.

Mitigation: Use environment variables or a secret manager, prefer test-mode or restricted read-only Stripe keys, and avoid pasting secrets directly into shell commands or source files.

Risk: Subscription metrics and deferred revenue schedules can affect investor reporting and accounting decisions if calculations or integration scope are misunderstood.

Mitigation: Independently review the metric formulas, accounting treatment, and claimed Chargebee or QuickBooks Online workflow before relying on outputs.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, Python, JSON, and tabular examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference Stripe, Chargebee, CSV, and QuickBooks Online workflows; users should verify financial calculations and credentials handling before use.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
