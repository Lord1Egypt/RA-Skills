## Description:

Automates daily diary creation by reading configured personal memory sources, writing a first-person diary entry, and exporting a 1080px-wide diary image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1204tmax](https://clawhub.ai/user/1204tmax)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to generate diary entries for a target date from configured SOUL, MEMORY, daily memory, recent diary, and optional news-summary context, then save the result as Markdown text and a shareable PNG image.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads private SOUL, MEMORY, daily memory, recent diary, and optional news-summary files as diary context.

Mitigation: Review config.yaml paths before use and disable optional sources that should not be included.

Risk: Generated diary text and PNG images may contain sensitive personal content intended for private use.

Mitigation: Inspect the generated Markdown before sharing the PNG image or moving outputs outside the configured diary directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1204tmax/skills/riji)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Configuration]

**Output Format:** [Markdown diary text, PNG image file, and a short result report with date, output paths, and image size]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configurable local paths and defaults to a 1080px image width.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
