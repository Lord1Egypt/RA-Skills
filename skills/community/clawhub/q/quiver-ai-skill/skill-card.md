## Description:

Generate SVGs from text prompts and convert raster images (PNG/JPG/WebP) to SVG using QuiverAI's AI models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lolieatapple](https://clawhub.ai/user/lolieatapple)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate SVG assets from text prompts or vectorize raster images for icons, illustrations, and logos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on installing and trusting the QuiverAI CLI.

Mitigation: Review the CLI before use and prefer a pinned or locally installed version.

Risk: API key setup may expose a QuiverAI key through local configuration or shell history.

Mitigation: Avoid pasting secrets into command history and manage the key with the least local exposure available.

Risk: Prompts, reference images, URLs, and raster files may be sent to QuiverAI services.

Mitigation: Do not process sensitive private files or private URLs without explicit approval.

Risk: Pass-through arguments and output paths can affect command behavior and file writes.

Mitigation: Review command arguments and confirm output paths before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lolieatapple/skills/quiver-ai-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and SVG file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill directs the agent to save generated or vectorized SVGs to .svg files, supports multiple variants, and reports the output path, file size, and a brief summary.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
