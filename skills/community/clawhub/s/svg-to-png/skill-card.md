## Description:

Converts SVG vector images to PNG files with an optional square output size.

This skill is ready for commercial/non-commercial use.

## Publisher:

[try520](https://clawhub.ai/user/try520)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and frontend engineers use this skill to convert SVG icons and application assets into PNG files, optionally resizing output for target resource dimensions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a reported vulnerable native image-processing dependency in the SVG-to-PNG conversion path.

Mitigation: Review before installing, update sharp to a non-vulnerable release with a regenerated lockfile, and run conversions for untrusted SVG files in a constrained environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/try520/skills/svg-to-png)
- [ClawHub publisher profile](https://clawhub.ai/user/try520)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [PNG file with terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts an input SVG path, optional output PNG path, and optional square size; defaults to 1024 pixels.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
