## Description:

Generate QR codes for strings or URLs using the QRClaw service, returning terminal-friendly UTF-8 QR output and a hosted smart link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emg110](https://clawhub.ai/user/emg110)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and end users use QR Claw to turn public or intentionally shareable strings, URLs, payment URIs, contact details, or workflow-generated links into scannable QR output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inputs are sent to an external QRClaw service and the generated smart link is publicly accessible for about 24 hours.

Mitigation: Use only public or intentionally shareable data; refuse passwords, API keys, tokens, private keys, personal identifiers, and other sensitive values.

Risk: Generated QR links expire after 24 hours and may not be suitable for long-lived distribution.

Mitigation: Tell users about the 24-hour expiry and regenerate QR codes when needed.

Risk: The QRClaw service is rate limited to 5 QR codes per minute per IP.

Mitigation: Avoid tight request loops; batch requests with delays or ask the user to retry after the limit resets.

## Reference(s):

- [QR Claw Skill Page](https://clawhub.ai/emg110/skills/qrclaw)
- [QRClaw Service](https://qrclaw.goplausible.xyz/)
- [QRClaw GitHub Project](https://github.com/GoPlausible/qrclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with a UTF-8 QR code block, original data, and smart link, or concise text link output for social channels]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated smart links expire after 24 hours; QR generation is rate limited to 5 requests per minute per IP.]

## Skill Version(s):

1.2.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
