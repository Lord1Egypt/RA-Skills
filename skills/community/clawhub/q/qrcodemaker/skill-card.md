## Description:

Generates and decodes QR codes for URLs, vCards, WiFi credentials, and plain text, with color customization and optional logo embedding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[starclimber](https://clawhub.ai/user/starclimber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to create QR code image files for URLs, WiFi networks, contact cards, and text, or to decode an existing QR image into text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated WiFi or vCard QR codes can disclose passwords or personal details to anyone who can scan the saved image.

Mitigation: Review the encoded content before sharing QR images and avoid placing sensitive QR files in public or broadly shared locations.

Risk: The Python dependencies are installed locally, and decoder support requires optional image-processing packages.

Mitigation: Install the skill in a virtual environment and review or pin dependencies before use.

## Reference(s):

- [Artifact README](artifact/README.md)
- [ClawHub skill page](https://clawhub.ai/starclimber/skills/qrcodemaker)

## Skill Output:

**Output Type(s):** [Files, Text, Shell commands, Guidance]

**Output Format:** [PNG image files, plain text decoder output, and Markdown command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation supports foreground and background colors, optional logo embedding, and URL, WiFi, vCard, and plain-text modes.]

## Skill Version(s):

1.0.4 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
