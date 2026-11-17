## Description:

QR code generation and reading for text, URLs, WiFi credentials, vCard contacts, image decoding, and batch generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yushimohuang](https://clawhub.ai/user/yushimohuang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate QR code PNGs for text, URLs, WiFi credentials, and vCard contacts, or to decode QR content from image files. It also supports batch generation from a text list.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WiFi QR generation can expose passwords in command output, shell history, logs, and generated PNG files.

Mitigation: Avoid real passwords in shell commands when possible, store generated PNGs in controlled locations, and delete sensitive QR files after use.

Risk: A filename handling issue may write WiFi QR images outside the intended default output folder.

Mitigation: Review generated output paths before sharing or retaining files, and use explicit controlled output locations.

Risk: Decoded QR content or contact QR data can contain sensitive personal information.

Mitigation: Treat decoded content and vCard QR images as sensitive and avoid logging or sharing them unnecessarily.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yushimohuang/skills/qr-code-toolkit)
- [Publisher profile](https://clawhub.ai/user/yushimohuang)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline shell commands and generated PNG files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated QR images are written to the default qrcodes folder or a caller-provided output path.]

## Skill Version(s):

1.0.0 (source: server release metadata and script header)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
