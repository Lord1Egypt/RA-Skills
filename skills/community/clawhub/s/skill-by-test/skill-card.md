## Description:

Create and manage test payment links for one-time, recurring, payment plans, multi-product, custom pricing, and donations in a sandbox environment.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[yaggit](https://clawhub.ai/user/yaggit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and testers use this skill to create sandbox payment-link flows, validate payment-link inputs, and inspect JSON-style responses without processing real payments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script sends payment data to a local HTTP API without authenticated HTTPS transport.

Mitigation: Use only local sandbox data, avoid live webhook endpoints, and require authenticated HTTPS or another secured local channel before production use.

Risk: The script contains a hard-coded placeholder API key and does not use the declared environment secret.

Mitigation: Remove the placeholder key and wire the declared secret into execution before any non-sandbox use.

Risk: Sandbox-only payment behavior could be mistaken for live payment processing.

Mitigation: Keep usage limited to test cards, mock data, and sandbox workflows; do not provide real cardholder, customer, or production API data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yaggit/skills/skill-by-test)
- [Skill homepage](https://test.com)

## Skill Output:

**Output Type(s):** [JSON, shell commands, guidance]

**Output Format:** [JSON API responses with concise error text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sandbox-only payment-link responses; raw tool responses should be preserved when applicable.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
