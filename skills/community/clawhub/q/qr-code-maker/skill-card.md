## Description:

QR code generator for text, URLs, WiFi, vCards, and other data with support for custom colors, sizes, logos, and PNG/SVG output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate QR code images for text, URLs, WiFi credentials, vCards, email, SMS, phone, and location data. It is useful when a workflow needs local QR generation with basic styling and optional logo embedding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WiFi QR codes can expose credentials or grant network access if shared too broadly.

Mitigation: Generate WiFi QR codes only for intended recipients and prefer guest-network credentials when possible.

Risk: The skill documentation claims broader format support than the security guidance confirms for the provided implementation.

Mitigation: Expect PNG output from the provided implementation and verify any SVG or PDF requirement before relying on it.

Risk: The skill depends on local Python packages for QR generation and image processing.

Mitigation: Install and run the dependencies in an isolated Python environment where practical.

## Reference(s):

- [Qr Generator ClawHub Skill](https://clawhub.ai/tobewin/skills/qr-code-maker)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell command code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local QR code image files through generated Python commands; server security guidance notes that the provided implementation should be expected to produce PNG output.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
