## Description:

Uses Python's standard library to inspect PNG image quality, compare images, and create resized, cropped, or contact-sheet PNGs without Pillow or OpenCV.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oracis](https://clawhub.ai/user/oracis)

### License/Terms of Use:

MIT-0

## Use Case:

Designers and developers use this skill to diagnose blurry, banded, or discolored PNGs, compare versions, and prepare crops or contact sheets without installing image libraries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image output commands can overwrite an existing file at the selected output path.

Mitigation: Choose a new output filename or back up existing files before running commands with -o.

Risk: JPEG images are unsupported without conversion to PNG.

Mitigation: Convert JPEG inputs to PNG before inspection.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/oracis/skills/zero-dep-image-inspect)

## Skill Output:

**Output Type(s):** [Text, Shell commands, PNG images]

**Output Format:** [Text diagnostics and guidance, CLI commands, and PNG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local PNG processing; JPEG images require conversion to PNG first.]

## Skill Version(s):

1.0.1 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
