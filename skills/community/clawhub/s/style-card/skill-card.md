## Description:

Reverse-engineers a reference image into a reusable style card, then uses that card to create new images in the same visual style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bonniegeng-max](https://clawhub.ai/user/bonniegeng-max)

### License/Terms of Use:

MIT

## Use Case:

Creators and designers use this skill to turn a reference image's visual style into a reusable, editable card, then apply it to new text and image requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The PNG export helper can silently install an unpinned Playwright package globally.

Mitigation: Review the helper and install a pinned Playwright version in a project-local environment before exporting images.

Risk: The documented HTML workflow requests Google Fonts, and reverse-analysis may send reference images or prompts to a model provider.

Mitigation: Use approved local fonts where possible, and avoid sending confidential images or prompts to external providers unless their data handling is acceptable.

Risk: Static checks could not inspect the bundled binary images, so evidence about their contents is incomplete.

Mitigation: Review bundled image assets before relying on them or redistributing them.

## Reference(s):

- [ClawHub release](https://clawhub.ai/bonniegeng-max/skills/style-card)
- [Style card reverse-analysis prompt](artifact/references/reverse-meta-prompt.md)
- [HTML output template guidance](artifact/references/html-template.md)
- [Generation gotchas and mitigations](artifact/gotchas.md)
- [Acknowledged workflow inspiration: frontend-slides](https://github.com/zarazhangrui/frontend-slides)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Images]

**Output Format:** [Markdown style cards and prompts, single-file HTML, PNG images, and optional animation-ready HTML.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Style cards use named content slots and include palette, layout, typography, and negative constraints. Image outputs depend on the selected generation engine.]

## Skill Version(s):

1.1.0 (source: frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
