## Description:

Prepare images and videos for a website or app - convert photos to WebP or AVIF, resize them to sensible widths with responsive variants, strip camera and location data, and turn videos into small streaming-friendly MP4 (H.264, faststart) or WebM with a poster image. Use when the user wants faster pages, smaller images, "optimize images", a hero or background video, or media for a web project.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tariksucu](https://clawhub.ai/user/tariksucu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers preparing images and videos for websites or apps can use this skill to convert, resize, and optimize media, create responsive variants and video posters, and add suitable web markup while preserving originals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The conversion fallback may send media to a third party without clearly disclosing this or warning the user first, which matters especially for private media.

Mitigation: Explain what media would be sent and get the user's consent before using remote conversion; keep private media local unless the user approves sharing it.

Risk: The security scan is partial because several local path-like references could not be resolved, so its evidence is incomplete.

Mitigation: Review the unresolved references and complete a security review before deployment.

## Reference(s):

- [Source repository (server-resolved provenance)](https://github.com/tariksucu/converter-studio/tree/main/skills/web-ready-media)
- [Converter Studio](https://converter.studio)
- [ClawHub release](https://clawhub.ai/tariksucu/skills/web-ready-media)

## Skill Output:

**Output Type(s):** [Markdown guidance, Shell commands, HTML code, Media conversion and optimization instructions]

**Output Format:** [Markdown with shell commands, HTML snippets, and reporting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommends preserving originals and reporting output dimensions, file sizes, and savings.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
