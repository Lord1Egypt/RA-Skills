## Description:

Generates Xiaohongshu (Little Red Book) infographic series with selectable visual styles and layouts, splitting user-provided content into social-media-ready image plans and prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dhready](https://clawhub.ai/user/dhready)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and content teams use this skill to turn articles, notes, or pasted content into Xiaohongshu-style infographic series with matching visual style, layout, outline, and generation prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan flags prompt language that tells image tools not to refuse sensitive or copyrighted figures.

Mitigation: Review or remove that prompt language before deployment and apply the host agent's normal content-safety and copyright controls.

Risk: The skill saves local output files and can use persistent preferences, including watermark text.

Mitigation: Use project-scoped preferences for shared workspaces, avoid storing private watermark text, and review generated files before publishing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dhready/skills/xhs-images-generator)
- [Homepage from metadata/clawdis](https://github.com/JimLiu/baoyu-skills#baoyu-xhs-images)
- [Style Presets](references/style-presets.md)
- [Canvas and Layout Elements](references/elements/canvas.md)
- [Prompt Assembly Workflow](references/workflows/prompt-assembly.md)
- [Analysis Framework](references/workflows/analysis-framework.md)
- [Preferences Schema](references/config/preferences-schema.md)
- [Watermark Guide](references/config/watermark-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance, outline files, prompt files, optional local configuration, and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a per-topic local output directory for source copies, analysis, outlines, prompts, and generated images.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence and target metadata; artifact frontmatter states 1.56.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
