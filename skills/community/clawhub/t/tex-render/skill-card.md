## Description:

Renders LaTeX math to PNG, JPEG, WebP, or AVIF images using MathJax and @svg-fns/svg2img when an agent needs to show equations, formulas, or notation as viewable images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thebigoranger](https://clawhub.ai/user/thebigoranger)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to convert LaTeX math into image files so equations can be shown directly in chat, documents, or slides instead of as raw LaTeX.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically render LaTeX without per-use confirmation when its automatic trigger is enabled.

Mitigation: Enable the automatic trigger only when that behavior is acceptable, or disable it when raw LaTeX or explicit confirmation is preferred.

Risk: The skill runs local Node.js rendering and requires npm install for public npm dependencies, including a native Sharp dependency.

Mitigation: Install and run it in a low-privilege or isolated workspace, and review resolved dependency versions before deployment.

Risk: Rendered SVG and image files are written to local output paths.

Mitigation: Use controlled output paths and avoid rendering sensitive formulas in shared workspaces.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thebigoranger/skills/tex-render)
- [MathJax](https://github.com/mathjax/MathJax)
- [@svg-fns/svg2img](https://github.com/svg-fns/svg-fns)
- [Sharp Install Notes](https://sharp.pixelplumbing.com/install)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands, Guidance]

**Output Format:** [JSON line with SVG and raster image paths, or a Data URL when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output writes SVG plus PNG under ~/.openclaw/media/tex-render; JPEG, WebP, AVIF, width, height, zoom, quality, and inline rendering are supported.]

## Skill Version(s):

1.1.4 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
