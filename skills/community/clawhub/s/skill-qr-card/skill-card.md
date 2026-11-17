## Description:

Generate styled QR images/cards for ClawHub skills so users can scan and install instantly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackleeio](https://clawhub.ai/user/jackleeio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill to create share-ready QR card assets that let users scan to install a ClawHub skill, open its ClawHub page, or open a related GitHub repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generator exposes a local command-execution risk through custom output paths when PNG conversion is enabled.

Mitigation: Review before installing, use trusted simple output filenames or disable PNG conversion, and constrain output paths before broad use.

## Reference(s):

- [Design Guidelines](references/design-guidelines.md)
- [ClawHub Skill Page](https://clawhub.ai/jackleeio/skills/skill-qr-card)

## Skill Output:

**Output Type(s):** [files, shell commands, markdown, guidance]

**Output Format:** [SVG file path with optional PNG file path and MEDIA lines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces SVG by default; PNG export depends on ImageMagick convert availability.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
