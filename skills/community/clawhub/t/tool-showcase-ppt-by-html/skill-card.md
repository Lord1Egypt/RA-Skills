## Description:

Generates single-file HTML web presentation decks for showcasing tools or apps, with horizontal slides, product-focused layouts, theme presets, animated backgrounds, and screenshot fallback handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suenkv](https://clawhub.ai/user/suenkv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product makers, and content creators use this skill to turn tool or app details, screenshots, links, and product messaging into polished browser-based showcase decks for launches, demos, GitHub Pages, README-adjacent promotion, and internal sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated decks automatically load mutable third-party JavaScript and external fonts.

Mitigation: Review generated decks before sharing or opening them in sensitive contexts; prefer vendoring a pinned Lucide release, using local or system fonts, or adding exact version and integrity controls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/suenkv/skills/tool-showcase-ppt-by-html)
- [Template HTML](artifact/assets/template.html)
- [Checklist](artifact/references/checklist.md)
- [Layouts](artifact/references/layouts.md)
- [Themes](artifact/references/themes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTML, CSS, and JavaScript snippets for a single-file presentation deck]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated decks may reference local image assets under an images directory and can include fallback placeholders for missing screenshots.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
