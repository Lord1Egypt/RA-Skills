## Description:

AI机票预订助手 helps users search Chinese domestic flights, compare fare classes, create flight booking orders, manage flight changes, and request refunds through the Fenbeitong flight workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryan-zry](https://clawhub.ai/user/ryan-zry)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-support agents use this skill to search Chinese domestic flights, compare fare and refund/change rules, create bookings, view orders, cancel unpaid orders, and submit change or refund requests after user confirmation.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill handles passenger identity data, phone numbers, credentials, payments, refunds, and order details.

Mitigation: Use it only in the intended Fenbeitong flight workflow, store credentials in a user-private secret store, and redact passenger identity data from outputs and logs.

Risk: The security guidance calls out unsafe API transport choices and endpoint handling.

Mitigation: Fix TLS verification and lock API traffic to an approved endpoint before operational use.

Risk: Booking, cancellation, change, and refund actions can affect real travel orders and payment flows.

Mitigation: Require explicit user confirmation before booking, cancellation, change, or refund actions.

Risk: Inherited environment variables may be untrusted in shared or managed environments.

Mitigation: Avoid shared machines for this skill and run it only where environment variables and local credential storage are controlled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryan-zry/skills/search-flight)
- [Publisher profile](https://clawhub.ai/user/ryan-zry)
- [Fenbeitong flight API endpoint](https://app-gate.fenbeitong.com/air_biz/skill/execute)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with plaintext tables and shell command invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write temporary JSON state files under /tmp and store authentication data in a local .fbt_auth.json file.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, skill.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
