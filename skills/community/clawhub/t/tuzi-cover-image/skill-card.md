## Description:

Generates article cover images with 5 dimensions (type, palette, rendering, text, mood) combining 9 color palettes and 6 rendering styles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ljquan](https://clawhub.ai/user/ljquan)

### License/Terms of Use:


## Use Case:

External users, creators, and developers use this skill to turn article content into cover-image prompts and local image outputs with controlled style dimensions, aspect ratios, optional reference images, and reusable preferences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can save article drafts, generated prompts, copied reference images, derived reference descriptions, and cover images in local output folders.

Mitigation: Review output paths and avoid providing sensitive source or reference material unless local storage is acceptable.

Risk: Project or user preference files can affect future generations, including watermark, quick mode, output location, language, and style defaults.

Mitigation: Prefer project-level preferences for project-specific settings and review EXTEND.md before reuse across unrelated work.

Risk: Quick mode can skip confirmation of style dimensions before image generation.

Mitigation: Disable quick mode when users need to review palette, rendering, text, mood, font, or aspect choices before generation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ljquan/skills/tuzi-cover-image)
- [Auto-Selection Rules](references/auto-selection.md)
- [Style Presets](references/style-presets.md)
- [Compatibility Matrices](references/compatibility.md)
- [Preferences Schema](references/config/preferences-schema.md)
- [Prompt Template](references/workflow/prompt-template.md)
- [Reference Image Handling](references/workflow/reference-images.md)
- [Visual Elements](references/visual-elements.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, image]

**Output Format:** [Markdown prompts, local configuration, copied source/reference files, completion text, and PNG cover images]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local output folders containing source content, reference assets, prompt files, and generated cover images.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
