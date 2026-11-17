## Description:

Discover and retrieve services and data via the RedotPay CLI across media, model APIs, data APIs, and commerce lookups without purchase flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[turbo-wang](https://clawhub.ai/user/turbo-wang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search RedotPay services, inspect endpoint schemas and pricing, and retrieve data through the RedotPay CLI. Paid requests require explicit confirmation, login only at request time, and a spend cap.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The first-time setup references a remote installer and an ineffective checksum check.

Mitigation: Install RedotPay from a trusted, signed release or package manager and verify the exact installer or binary digest independently before use.

Risk: Paid service requests can spend funds or expose sensitive wallet/payment metadata if run without clear review.

Mitigation: Run paid requests only after the service, endpoint, price, spend cap, and purpose are clear and the user has explicitly confirmed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/turbo-wang/skills/redotpay)
- [RedotPay CLI installer reference](https://raw.githubusercontent.com/redotpay/redotpay-cli/v0.1.0/install.sh)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and JSON-oriented CLI output references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the redotpay CLI; paid requests require service, endpoint, price, spend cap, purpose, and user confirmation before execution.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
