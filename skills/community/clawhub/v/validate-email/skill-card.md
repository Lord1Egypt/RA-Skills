## Description:

Validate email addresses with format checking, disposable-domain detection, domain extraction, and local risk scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kennyzir](https://clawhub.ai/user/kennyzir)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to pre-check individual or bulk email inputs for basic format validity, disposable-domain signals, and lightweight risk scoring before downstream workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hosted SDK and fetch examples can send email addresses and API credentials to an external service despite local privacy claims.

Mitigation: Use the local validation path for private or bulk email data; adopt hosted examples only after explicitly accepting external data transfer and API key handling requirements.

Risk: Validation is limited to syntax checks, built-in domain lists, and local scoring, so it does not prove mailbox existence or deliverability.

Mitigation: Treat results as a pre-filter and use a dedicated deliverability check when MX records, SMTP acceptance, or bounce risk matter.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kennyzir/skills/validate-email)
- [Publisher profile](https://clawhub.ai/user/kennyzir)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [JSON object with validation checks, normalized email, risk score, and optional suggestion]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally and returns deterministic format and risk checks without SMTP, DNS MX, or deliverability verification.]

## Skill Version(s):

1.0.1 (source: evidence.release.version and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
