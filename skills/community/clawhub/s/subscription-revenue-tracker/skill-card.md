## Description: <br>
SaaS and subscription business revenue intelligence for tracking MRR/ARR, churn, net revenue retention, LTV, cohort retention, payback periods, investor summaries, and deferred revenue journal entries from Stripe, Chargebee, or CSV exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance, SaaS operations, and accounting users can use this skill to calculate subscription KPIs, prepare investor updates, analyze cohort retention, and draft deferred revenue schedules or QBO-ready journal entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may work with subscription billing API keys and customer revenue data. <br>
Mitigation: Use restricted or read-only API keys where possible, keep secrets in environment variables or a secret manager, and redact customer exports before sharing them with an agent. <br>
Risk: Generated deferred revenue or accounting entries could be incorrect if source data, dates, or revenue recognition assumptions are wrong. <br>
Mitigation: Manually review generated accounting entries and revenue schedules before posting them to QuickBooks Online or any general ledger. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/samledger67-dotcom/subscription-revenue-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/samledger67-dotcom) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with metric tables, Python and shell code blocks, API examples, and structured accounting entry examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference Stripe, Chargebee, QuickBooks Online, CSV exports, and local command-line tools when the user supplies appropriate data and credentials.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
