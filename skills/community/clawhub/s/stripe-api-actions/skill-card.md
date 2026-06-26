## Description: <br>
Use Stripe's live REST API for authenticated write actions. Use when you need to create or update Stripe customers, products, prices, payment links, refunds, subscriptions, or metadata with a secret key supplied via STRIPE_SECRET_KEY. Keep this separate from read-only inspection when the task changes live billing or payment state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stanestane](https://clawhub.ai/user/stanestane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to perform authenticated Stripe write actions for customers, products, prices, payment links, refunds, subscription cancellation, and metadata updates. It is intended for tasks that change live billing or payment state and require explicit confirmation before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make live Stripe billing and payment changes. <br>
Mitigation: Install only for workflows that intentionally require Stripe write access, use restricted Stripe keys when possible, and require explicit --confirm for each write command. <br>
Risk: Refunds and subscription cancellations can affect live money flow or customer billing state. <br>
Mitigation: Verify object IDs, amounts, and cancellation intent outside the agent before executing refunds or subscription cancellations. <br>
Risk: The metadata update command can post to overly broad Stripe API paths when supplied with a secret key. <br>
Mitigation: Use update_metadata only for known intended object paths such as customers or products, and avoid arbitrary paths. <br>


## Reference(s): <br>
- [Stripe API Actions and Safety](references/actions-and-safety.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/stanestane/stripe-api-actions) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires STRIPE_SECRET_KEY and --confirm for write actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
