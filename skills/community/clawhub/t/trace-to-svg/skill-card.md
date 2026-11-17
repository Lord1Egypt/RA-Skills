## Description:

Trace bitmap images (PNG/JPG/WebP) into clean SVG paths using potrace/mkbitmap.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajmwagar](https://clawhub.ai/user/ajmwagar)

### License/Terms of Use:


## Use Case:

Developers and fabrication-oriented engineers use this skill to convert high-contrast bitmap logos, silhouettes, and reference images into SVG paths for downstream vector and CAD workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow requires installing and running the local potrace command-line tools.

Mitigation: Install potrace from the declared package manager source and confirm both potrace and mkbitmap are available before running the skill.

Risk: The script can create or overwrite SVG files at the output path provided by the user.

Mitigation: Choose an explicit output path where replacement is acceptable and review generated files before using them downstream.

Risk: Tracing quality depends heavily on image contrast and threshold settings, especially for photos or complex shading.

Mitigation: Prefer high-contrast source images and adjust threshold, turdsize, alphamax, and opttolerance before using the result in CAD or manufacturing workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ajmwagar/skills/trace-to-svg)
- [Examples](references/examples.md)
- [Publisher Profile](https://clawhub.ai/user/ajmwagar)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Guidance]

**Output Format:** [Markdown with inline bash commands and SVG file/path references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or overwrites SVG files at explicitly provided output paths and requires local potrace and mkbitmap binaries.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
