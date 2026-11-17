## Description:

Generate SVG images using text LLM instead of image generation APIs for illustrations, icons, cartoons, diagrams, and other simple visual content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juliantsaiii](https://clawhub.ai/user/juliantsaiii)

### License/Terms of Use:


## Use Case:

Developers, designers, and agent users use this skill to generate simple SVG-based visual assets and convert them to PNG when image generation APIs are unavailable or unnecessary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can turn a crafted output filename into arbitrary shell command execution.

Mitigation: Review before installing; avoid running artifact/scripts/generate_svg.js with filenames or paths supplied by untrusted users, prompts, or external content.

Risk: Generated SVG guidance may produce incorrect, unsafe, or unsuitable visual output for the intended use case.

Mitigation: Review generated SVG and converted images before deployment, publication, or reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juliantsaiii/skills/svg-artist)
- [Publisher profile](https://clawhub.ai/user/juliantsaiii)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown with SVG, JavaScript, and shell command snippets; generated SVG and PNG files when executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Intended for cartoons, icons, simple illustrations, stylized art, and simple scenes rather than photorealistic or highly detailed images.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
