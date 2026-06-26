## Description: <br>
Complete read-only Stripe analytics dashboard for SaaS founders, covering recurring revenue, churn, customer segments, revenue recovery, forecasts, and actionable insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomas-mikula](https://clawhub.ai/user/tomas-mikula) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
SaaS founders and operators use this skill to fetch read-only Stripe metrics, customer segments, churn signals, forecasts, and action items from a restricted Stripe key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive revenue and customer data through broad text or voice triggers. <br>
Mitigation: Use explicit slash commands where possible and require confirmation before fetching or speaking Stripe data, especially in shared or voice-driven agents. <br>
Risk: A Stripe key with excessive permissions could expand the impact of accidental or unauthorized use. <br>
Mitigation: Use only a restricted read-only Stripe key scoped to customers, subscriptions, invoices, and payment intents. <br>


## Reference(s): <br>
- [Stripe API keys documentation](https://docs.stripe.com/keys) <br>
- [Stripe Analytics on ClawHub](https://clawhub.ai/tomas-mikula/stripe-analytics) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [JSON status object with metrics, insights, action items, and execution metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires STRIPE_READ_KEY and returns bounded read-only Stripe analytics for the requested time window.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
