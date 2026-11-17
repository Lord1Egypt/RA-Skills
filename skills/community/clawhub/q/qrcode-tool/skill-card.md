## Description:

Generate QR codes from URLs or text. Export as PNG with customizable size. No API key required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can generate QR code images from URLs, plain text, contact links, phone links, or Wi-Fi payloads with configurable size, margin, and image format.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Encoded text is sent to api.qrserver.com, which can expose passwords, tokens, internal URLs, contact details, or Wi-Fi credentials.

Mitigation: Use only nonsensitive payloads with this skill, or use a trusted local QR generator for confidential data.

Risk: JSON output includes the generated request URL, which can preserve the encoded payload in logs or downstream records.

Mitigation: Avoid JSON mode for sensitive content and redact generated URLs before logging or sharing output.

## Reference(s):

- [qrserver.com API](https://api.qrserver.com)
- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/qrcode-tool)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; the script can print text status or JSON and returns base64-encoded image data when used programmatically.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated QR payloads are requested from api.qrserver.com; PNG, GIF, JPEG, and JPG formats are supported by the script.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
