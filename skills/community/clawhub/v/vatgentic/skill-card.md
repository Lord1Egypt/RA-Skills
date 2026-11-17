## Description:

Instant EU VAT validation with Lightning Bitcoin. 10 sats per lookup. No subscriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mcclawd](https://clawhub.ai/user/mcclawd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to request EU VAT-number validation, pay the Lightning invoice, and retrieve validity, company name, address, and country-code details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: VAT numbers may be business-sensitive and are sent to a configured external VatGentic service.

Mitigation: Use only trusted endpoints and confirm that the organization is allowed to submit VAT numbers to that service.

Risk: Lightning invoices and optional wallet credentials can create spending exposure if automated payment flows are configured carelessly.

Mitigation: Keep automated payments disabled unless the operator understands the wallet setup, limits payment amounts, and accepts the spending risk.

Risk: Live validation depends on external API, payment, and status endpoints that may fail or be misconfigured.

Mitigation: Check service status, handle pending or failed requests, and verify the end-to-end flow before relying on results in production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mcclawd/skills/vatgentic)
- [ClawHub publisher profile](https://clawhub.ai/user/mcclawd)
- [VatGentic documentation](https://docs.vatgentic.com)
- [VatGentic status](https://status.vatgentic.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell examples, plus optional JSON API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured VatGentic API endpoint and Lightning payment flow for live validation.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
