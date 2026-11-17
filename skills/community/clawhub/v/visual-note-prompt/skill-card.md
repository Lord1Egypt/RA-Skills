## Description:

Generates standardized image prompts that turn short text into visual knowledge-card notes, with content splitting, style selection, layout selection, and strict formatting rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spiderzhcl](https://clawhub.ai/user/spiderzhcl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to turn short learning notes, summaries, or concept explanations into standardized visual knowledge-card image prompts for image generators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated prompts include a fixed third-party author mark in every image prompt.

Mitigation: Remove or override the author field before using generated prompts for neutral, client-owned, or publication-ready images.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spiderzhcl/skills/visual-note-prompt)
- [视觉笔记提示词格式指南](artifact/references/format-guide.md)
- [视觉风格与构图库](artifact/assets/style-library.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown prompt blocks with structured image-generation fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one or more visual note image prompts; generated prompts include a fixed `By 八点虾` author field.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
