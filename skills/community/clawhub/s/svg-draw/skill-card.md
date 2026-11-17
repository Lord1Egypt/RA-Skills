## Description:

Create SVG images and convert them to PNG without external graphics libraries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lijy2015](https://clawhub.ai/user/lijy2015)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to draft SVG artwork, customize bundled dragon and lobster templates, and convert SVG outputs to PNG images for user-requested sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SVG or PNG files may overwrite existing workspace files if paths are reused.

Mitigation: Use explicit workspace paths and check before writing or converting output files.

Risk: Generated images may be shared to external channels unintentionally.

Mitigation: Only send generated SVG or PNG files externally when the user explicitly asks for sharing.

Risk: PNG conversion depends on local rsvg-convert availability and valid file paths.

Mitigation: Confirm rsvg-convert is installed and validate input and output paths before invoking the converter.

## Reference(s):

- [SVG Draw ClawHub page](https://clawhub.ai/lijy2015/skills/svg-draw)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Guidance, Files]

**Output Format:** [SVG/XML code with optional shell commands for PNG conversion]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [PNG conversion uses local rsvg-convert with caller-provided input and output paths plus optional width and height.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
