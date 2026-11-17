## Description:

QR-based skill installer for ClawHub that decodes QR images, extracts a valid skill slug or install command, and installs via the ClawHub CLI after user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackleeio](https://clawhub.ai/user/jackleeio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ClawHub users use this skill to install a skill from a QR image, screenshot, or camera capture after reviewing the decoded target. It supports scan-to-install workflows where the agent should report the decoded text, parsed slug, install command, and result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A QR payload may point to an unintended ClawHub skill or use plain command text that the user has not verified.

Mitigation: Show the decoded text and parsed slug before installation, require explicit confirmation, and recommend checking unfamiliar skills on ClawHub first.

Risk: Installing a skill modifies the user's local ClawHub skill set.

Mitigation: Use the dry-run default until the user confirms, and install only skills from sources the user trusts.

## Reference(s):

- [Slug Parsing Rules](references/slug-parsing.md)
- [ClawHub skill page](https://clawhub.ai/jackleeio/skills/scan-to-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown status output with decoded QR text, parsed slug, install command, result, and next-step guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Installation remains gated by explicit user confirmation; dry-run and decode-only flows can report results without modifying the local ClawHub skill set.]

## Skill Version(s):

0.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
