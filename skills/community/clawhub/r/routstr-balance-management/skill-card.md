## Description:

Manage Routstr balance by checking balance, creating Lightning invoices for top-up, and checking invoice payment status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sh1ftred](https://clawhub.ai/user/sh1ftred)

### License/Terms of Use:

MIT

## Use Case:

Developers and Routstr users use this skill to check account balance and usage, create Lightning invoices for top-ups, check invoice status, and submit Cashu tokens for balance top-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scripts handle Routstr API keys and payment tokens for balance-management actions.

Mitigation: Run only on a trusted machine and use a Routstr API key you are comfortable exposing to these scripts.

Risk: Cashu tokens are placed in a request URL, where they may be logged or visible in process metadata.

Mitigation: Avoid using Cashu tokens with this version until the top-up flow sends the token through a safer channel.

Risk: Invoice amount handling needs validation and unit alignment before relying on it for payments.

Mitigation: Review and fix the invoice script to validate amounts and confirm expected units before payment use.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads Routstr API configuration from ~/.openclaw/openclaw.json and prints balance, invoice, payment-status, or top-up results.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
