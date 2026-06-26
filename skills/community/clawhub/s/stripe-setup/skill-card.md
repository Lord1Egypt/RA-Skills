## Description: <br>
Adds Stripe payments to agent-built apps with checkout sessions, subscription billing, webhook handling, customer portal setup, and test-mode validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ferrentinomj-dev](https://clawhub.ai/user/ferrentinomj-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add and test Stripe checkout, subscriptions, webhooks, and customer billing portal flows in Python Flask apps, with guidance they can adapt to FastAPI, Express, serverless, or other web stacks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment setup can affect live billing and customer access. <br>
Mitigation: Use Stripe test mode first, review live-mode changes carefully, and validate checkout, subscription, cancellation, and payment-failure flows before switching to live keys. <br>
Risk: Stripe secret keys and webhook signing secrets could be exposed or misconfigured. <br>
Mitigation: Keep secret keys server-side in environment variables, use separate test and live webhook secrets, and require webhook signature verification. <br>
Risk: Stripe CLI installation commands add an external package repository and key. <br>
Mitigation: Verify the repository and key commands against Stripe's official CLI installation documentation before running them. <br>


## Reference(s): <br>
- [Stripe Python SDK docs](https://stripe.com/docs/api?lang=python) <br>
- [Checkout Session API](https://stripe.com/docs/api/checkout/sessions) <br>
- [Webhook events reference](https://stripe.com/docs/api/events/types) <br>
- [Stripe CLI](https://stripe.com/docs/stripe-cli) <br>
- [Customer Portal](https://stripe.com/docs/billing/subscriptions/customer-portal) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes environment variable examples, Flask-oriented Stripe helper code, webhook handling patterns, and go-live checklist guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
