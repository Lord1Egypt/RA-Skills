## Description: <br>
Stripe revenue dashboard in your agent for MRR, churn, new subscriptions, failed payments, and alerts when an operator asks about Stripe revenue or activity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ordo-tech](https://clawhub.ai/user/ordo-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operators, founders, and revenue teams use this skill to ask an agent for Stripe revenue status, subscription trends, failed-payment checks, product revenue, scheduled daily summaries, and alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Stripe credentials and may request more Stripe authority than a read-only dashboard needs. <br>
Mitigation: Use a Stripe restricted read-only key scoped to the documented resources, and avoid full live secret keys unless explicitly approved. <br>
Risk: Scheduled summaries, polling, webhooks, or Telegram alerts may expose revenue, customer, or failed-payment details outside the local agent context. <br>
Mitigation: Keep summaries local by default, approve any external delivery channel intentionally, and omit customer names, descriptions, and detailed failed-payment data from alerts. <br>
Risk: Webhook mode requires a publicly reachable OpenClaw instance and an additional signing secret. <br>
Mitigation: Enable webhook mode only when the endpoint exposure and STRIPE_WEBHOOK_SECRET handling are understood and reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ordo-tech/skill-stripe-monitor) <br>
- [Stripe API keys](https://dashboard.stripe.com/apikeys) <br>
- [Stripe status](https://status.stripe.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Stripe revenue metrics, subscription counts, failed-payment summaries, alert text, and setup guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
