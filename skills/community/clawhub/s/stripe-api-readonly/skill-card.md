## Description: <br>
Use Stripe's live REST API for authenticated account inspection and operational lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stanestane](https://clawhub.ai/user/stanestane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect a Stripe account with an authenticated secret key, list common payment and billing objects, retrieve known objects, and search customers through read-only commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A live Stripe secret key can expose sensitive business, customer, payment, invoice, payout, dispute, and webhook data. <br>
Mitigation: Use the most restricted Stripe key available, keep keys out of chat and files, rotate any exposed key, and review outputs before sharing them. <br>
Risk: The skill connects to the live Stripe account tied to STRIPE_SECRET_KEY. <br>
Mitigation: Verify the target account before inspection and default to the documented read-only commands. <br>


## Reference(s): <br>
- [Stripe API Objects and Workflows](references/objects-and-workflows.md) <br>
- [Stripe API endpoint](https://api.stripe.com/v1) <br>
- [ClawHub skill page](https://clawhub.ai/stanestane/stripe-api-readonly) <br>
- [Publisher profile](https://clawhub.ai/user/stanestane) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses from Stripe] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Stripe API inspection output may contain account, customer, payment, invoice, payout, dispute, and webhook data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
