## Description:

Generate QR codes from text, URLs, or data as PNG images for payments, WiFi sharing, or other scannable content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shixiaoliuo](https://clawhub.ai/user/shixiaoliuo)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to turn provided text, URLs, payment details, WiFi sharing strings, or other data into a scannable QR code image.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The QR generator can overwrite arbitrary writable files if an unsafe output path is supplied.

Mitigation: Use explicit dedicated output paths, avoid paths from untrusted content, and confirm before overwriting existing files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shixiaoliuo/skills/qrcode-generator)

## Skill Output:

**Output Type(s):** [text, shell commands, files]

**Output Format:** [PNG image file with text file-path output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a QR code PNG to the default qrcode.png path or to a caller-provided output path.]

## Skill Version(s):

1.0.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
