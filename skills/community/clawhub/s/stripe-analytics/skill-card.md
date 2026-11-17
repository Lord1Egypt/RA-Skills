## Description:

Provides a read-only Stripe analytics dashboard for SaaS revenue, churn, customer, forecast, and action-item insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomas-mikula](https://clawhub.ai/user/tomas-mikula)

### License/Terms of Use:

MIT-0

## Use Case:

SaaS founders, operators, and developers use this skill to inspect Stripe billing data and produce revenue dashboards, churn analysis, customer rankings, forecasts, and operational alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads sensitive Stripe customer and revenue data.

Mitigation: Use only a narrowly scoped Stripe restricted key with read permissions for customers, subscriptions, invoices, and payment intents.

Risk: Some dashboard claims and metrics may be simplified or hard-coded.

Mitigation: Treat generated metrics as decision-support output and verify important financial figures against Stripe or accounting systems before use.

Risk: Broad voice or shortcut triggers could expose billing analytics unintentionally.

Mitigation: Use execution environments that require confirmation before invoking the skill or displaying sensitive results.

## Reference(s):

- [Stripe API keys documentation](https://docs.stripe.com/keys)
- [ClawHub skill page](https://clawhub.ai/tomas-mikula/skills/stripe-analytics)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON analytics response with status, data, and metadata fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires STRIPE_READ_KEY and returns read-only Stripe metrics, forecasts, alerts, and action items.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
