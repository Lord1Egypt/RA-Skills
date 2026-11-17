## Description:

Generates polished single-file HTML presentation decks with reusable themes, layouts, mobile-friendly behavior, and optional preview/PDF export support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and business users use this skill to turn outlines, reports, pitch decks, product launches, technical talks, and other presentation content into ready-to-run HTML slide decks. It is especially suited for visually polished web-based presentations that need stable themes, reusable layouts, local generation, and mobile-friendly viewing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release declares an unnecessary unpinned global npm dependency that can run code during installation.

Mitigation: Review or remove the global npm dependency before installing, and pin or vendor any dependency that remains required.

Risk: Preview rendering can process HTML and scripts create or overwrite output files.

Mitigation: Render only HTML produced by the skill or otherwise trusted content, and choose output paths carefully before running preview or generation scripts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tobewin/skills/web-slides)
- [Runtime](artifact/references/runtime.md)
- [Theme Catalog](artifact/references/theme-catalog.md)
- [Layout System](artifact/references/layout-system.md)
- [Content Schema](artifact/references/content-schema.md)
- [Assembly Workflow](artifact/references/assembly-workflow.md)
- [Quality Bar](artifact/references/quality-bar.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTML, JSON, and shell command snippets; generated artifacts are single-file HTML decks and optional PNG previews.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local Node-based scripts, predefined themes, structured content JSON, embedded CSS, lightweight JavaScript navigation, and optional headless Chrome preview rendering.]

## Skill Version(s):

2.0.4 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
