## Description:

Generate and export presentations using Slidev when a user explicitly asks for Slidev, Markdown slides, a previewable slides.md, or PDF/PPTX/HTML export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laofahai](https://clawhub.ai/user/laofahai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external OpenClaw users use this skill to create visually designed Slidev decks from topics or outlines, preview them locally, and export presentation deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or modify files in a local Slidev project.

Mitigation: Run it in a dedicated presentation directory and review generated slides and exported files before reuse.

Risk: Setup and export workflows can run npm installs, including export dependencies.

Mitigation: Review the bundled scripts first and pin or lock package versions in the Slidev project before exporting.

Risk: PPTX export is image-based and may not meet needs for editable PowerPoint files.

Mitigation: Confirm whether editable PPTX is required, test PDF export first, and disclose the image-based PPTX limitation to users.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/laofahai/skills/slidev-ppt-generator)
- [Slidev Documentation](https://cn.sli.dev/)
- [Slidev Theme Gallery](https://sli.dev/guide/theme-addon-gallery)
- [Presentation Design Notes](references/presentation-design.md)
- [Prompting Strategy](references/prompting.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Slidev Markdown decks with YAML frontmatter, inline code or shell commands, and optional exported presentation files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify a local Slidev project and export PDF, PPTX, PNG, HTML, or Markdown outputs depending on the user's request.]

## Skill Version(s):

1.4.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
