## Description:

QR code scanning and generation. Invoke when user needs to scan/decode QR codes from images, generate QR codes (text, URL, WiFi), or mentions QR code related tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moxin1044](https://clawhub.ai/user/moxin1044)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to decode QR codes from local images, URLs, or Base64 inputs and to generate QR codes for text, URLs, and WiFi credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URL scanning can make network requests from the agent environment.

Mitigation: Prefer local files or Base64 input for QR scanning, and only scan URLs from trusted sources.

Risk: Generated WiFi QR images embed network credentials.

Mitigation: Treat WiFi QR images and Base64 outputs as sensitive material and share or store them only through trusted channels.

## Reference(s):

- [qrcode-scan on ClawHub](https://clawhub.ai/moxin1044/skills/qrcode-scan)
- [python-qrcode](https://github.com/lincolnloop/python-qrcode)
- [pyzbar](https://github.com/NaturalHistoryMuseum/pyzbar)
- [pyzbar on PyPI](https://pypi.org/project/pyzbar/)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands, Code, Guidance]

**Output Format:** [Plain text or JSON for decoded QR content; PNG files or Base64 strings for generated QR codes; Markdown guidance with shell and Python examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can scan local files, URLs, Base64 image data, or bytes; WiFi QR generation embeds SSID, security type, and password in the generated code.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
