## Description: <br>
Stripe API integration with managed OAuth for administering customers, subscriptions, invoices, products, prices, payments, coupons, refunds, payment methods, and related billing resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and finance teams use this skill to inspect and administer Stripe billing resources through Maton-managed OAuth. It supports billing workflows that require account context checks and explicit approval for write operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write-capable Stripe actions can change billing data or trigger financial consequences. <br>
Mitigation: Require explicit human confirmation that includes endpoint, target resource, object IDs, amounts, and test or live mode before any write operation. <br>
Risk: A request can affect the wrong Stripe account when multiple connections exist. <br>
Mitigation: Always specify and verify the Maton connection ID before making requests. <br>
Risk: Excessive account permissions can broaden the impact of errors or misuse. <br>
Mitigation: Use the least-privileged Stripe connection available, prefer test mode for evaluation, and revoke unused connections promptly. <br>


## Reference(s): <br>
- [Stripe API Reference](https://docs.stripe.com/api) <br>
- [Stripe Testing](https://docs.stripe.com/testing) <br>
- [Maton](https://maton.ai) <br>
- [ClawHub Stripe Skill](https://clawhub.ai/byungkyu/stripe-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell, Python, JavaScript, HTTP endpoint, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a valid Maton-managed Stripe OAuth connection.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
