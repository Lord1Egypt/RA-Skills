## Description:

Generates editable scientific illustration SVGs from research method descriptions, with optional reference-image style transfer and browser-based SVG editing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidzhao30](https://clawhub.ai/user/davidzhao30)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, developers, and technical authors use this skill to turn long-form method descriptions into editable SVG figures, apply a reference visual style, and refine generated diagrams in an interactive editor.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation and runtime behavior may execute unreviewed remote code or dependencies.

Mitigation: Install in a virtual environment or container and pin external repositories and dependencies to reviewed versions before use.

Risk: The local editor may expose broad network access when bound to 0.0.0.0.

Mitigation: Bind the editor to localhost by default, add authentication and network controls before wider exposure, and avoid opening it on untrusted networks.

Risk: Scientific text, unpublished figures, or proprietary images may be sent to third-party AI providers or be affected by telemetry.

Mitigation: Do not submit sensitive research or proprietary images unless provider terms, data handling, and telemetry behavior have been reviewed and accepted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/davidzhao30/skills/scientific-drawing-skill-1-0-0)
- [AutoFigure-Edit project referenced by skill artifact](https://github.com/ResearAI/AutoFigure-Edit)
- [Segment Anything 3 reference from skill artifact](https://github.com/facebookresearch/segment-anything-3)
- [Google Gemini documentation referenced by skill artifact](https://ai.google.dev/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration examples, and generated figure file descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The described workflow produces editable SVG files, PNG previews, segmentation metadata, SVG templates, and extracted icon assets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
