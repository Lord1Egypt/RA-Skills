## Description:

SVG Studio helps agents author precise SVG images for posters, diagrams, charts, icons, and infographics, with optional PNG, HTML, GIF, APNG, WebP, or MP4 export through local scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dqsjqian](https://clawhub.ai/user/dqsjqian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content teams, and agent users use this skill to create editable SVG illustrations, charts, diagrams, posters, icons, and infographics when precise text, data, layout, and aspect ratio control matter. Users can optionally request local export to PNG, HTML, or animated formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The rendering scripts can write image, HTML, and animation files in the local workspace.

Mitigation: Run the skill in a workspace where generated files are expected, and review output paths before executing export commands.

Risk: The skill can download Python packages into a local virtual environment on first use.

Mitigation: Pin or vendor dependencies before production use, or review package installation in a controlled environment.

Risk: SVG rendering may launch a local browser with no-sandbox mode.

Mitigation: Render only SVGs you authored or trust, and avoid browser rendering of untrusted SVG input unless additional sandboxing is provided.

## Reference(s):

- [SVG Studio README](README.md)
- [SVG techniques and aspect ratio presets](references/svg-techniques.md)
- [Hand-drawn and product infographic style guide](references/handdrawn-infographic.md)
- [SVG animation workflow](references/animation.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with SVG, HTML, shell command examples, and generated image or animation files when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static image delivery defaults to SVG; PNG, HTML, GIF, APNG, WebP, and MP4 exports are optional request-driven outputs.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
