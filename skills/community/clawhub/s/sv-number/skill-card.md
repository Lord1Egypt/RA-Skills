## Description:

Order a private phone number in any country over the API, receive the SMS verification code, and hand the number back. Use when an agent has to pass a phone check during signup, login or account recovery, or needs a TOTP second factor computed locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sv-number](https://clawhub.ai/user/sv-number)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use SV Number to obtain temporary phone numbers and retrieve SMS verification codes for authorized signup or account access workflows. It can also calculate TOTP codes locally from a supplied secret.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this release suspicious with medium confidence; a possible environment-data network flow was disputed by its review, and only one of three components was fully inspected.

Mitigation: Review the skill’s tool scope and inspect its scripts before installation. Keep the API key in a secret store and confirm requests go only to sms-verification-number.com.

Risk: Temporary-number use may affect later account recovery or conflict with a service’s rules.

Mitigation: Check the target service’s rules and recovery options; do not use temporary numbers for banking, payment, or government services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sv-number/skills/sv-number)
- [SMS activation API documentation](https://sms-verification-number.com/en/api-sms-activate/)
- [SMS Number service](https://sms-verification-number.com)

## Skill Output:

**Output Type(s):** [Text, API Calls, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance, shell commands, Python or JavaScript code, and API response text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May handle activation details and single-use SMS or TOTP codes.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
