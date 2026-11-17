## Description:

Generate React design drafts (4-piece set) from content. Invoke for 'design draft'/'设计稿'/'生成页面'/'信息图'/'知识卡片'/'多图配图'. Do NOT use for editing existing code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardwason](https://clawhub.ai/user/edwardwason)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to turn structured article or knowledge-card content into editable React design drafts and illustration sets. It supports content parsing, style selection, chart guidance, generated React files, and post-generation editing guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shortcut modes can generate files automatically.

Mitigation: Review the generated file tree and proposed changes before adding the output to an existing project.

Risk: The skill may read an optional local brand profile or inspect style files in a project the user references.

Mitigation: Reference only projects and brand-profile files that are intended to inform the design draft.

Risk: The skill may use external stock image sources when fallback imagery is selected.

Mitigation: Confirm that selected image sources and licenses are appropriate for the target publication or release.

Risk: The workflow is oriented toward Chinese/CJK content and design conventions.

Mitigation: Check output language, typography, and layout choices when using it for non-CJK audiences.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/edwardwason/skills/react-design-draft)
- [React Design Draft Generator README](README.md)
- [React 4-Piece Output Specification](references/react-output-spec.md)
- [Content to Layout Mapping and Three-Dimension Combination System](references/content-layout-mapping.md)
- [Aesthetics Guide v3](references/aesthetics-guide.md)
- [Information Density Quantification Standards](references/density-standards.md)
- [Chart System](references/chart-system.md)
- [Multi-Illustration Mode](references/multi-illustration.md)
- [Brand Profile System](references/brand-profile.md)
- [Style Presets](references/style-presets.md)
- [Image Sources](references/image-sources.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with React project files, including CSS design tokens, data modules, JSX components, and preview structure.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended to be editable React design drafts rather than production application code.]

## Skill Version(s):

5.3.0 (source: frontmatter, changelog, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
