## Description:

Verifies phone numbers via SMS OTP using the Sendly Verify API. Sends codes, checks codes, handles expiry, and provides hosted verification sessions. Applies for phone verification, OTP, 2FA, or passwordless login flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sendly-live](https://clawhub.ai/user/sendly-live)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to add Sendly-backed phone verification, OTP, 2FA, or passwordless login flows to applications. It provides concise REST API and Node.js SDK examples for sending, checking, resending, and validating hosted verification sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an external SMS verification provider and requires a Sendly API key.

Mitigation: Confirm Sendly is the intended provider, protect SENDLY_API_KEY, and avoid exposing credentials in client code or logs.

Risk: Phone numbers, OTPs, and hosted session tokens are sensitive verification data.

Mitigation: Avoid logging OTPs or session tokens, validate hosted-session tokens server-side, and apply consent and retention rules for phone number data.

Risk: Real SMS messages may be sent during testing when production credentials are used.

Mitigation: Use Sendly sandbox keys for test workflows when real SMS delivery is not intended.

## Reference(s):

- [Verify API docs](https://sendly.live/docs/verify)
- [OTP tutorial](https://sendly.live/docs/tutorials/otp)
- [Error handling guide](https://sendly.live/docs/how-to/handle-otp-errors)
- [ClawHub skill page](https://clawhub.ai/sendly-live/skills/verifying-phones)
- [Publisher profile](https://clawhub.ai/user/sendly-live)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with TypeScript, Bash, JSON, and API workflow examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes REST and Node.js examples, environment variable guidance for SENDLY_API_KEY, sandbox testing notes, status handling, and error remediation guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
