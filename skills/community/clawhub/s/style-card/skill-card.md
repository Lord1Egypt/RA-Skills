## Description:

Reverse-engineers a reference image into a reusable style card, then applies saved style cards to generate new images from text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bonniegeng-max](https://clawhub.ai/user/bonniegeng-max)

### License/Terms of Use:

MIT

## Use Case:

Developers and creators use this skill to turn a reference image into a reusable visual style guide, then apply that style to new text or image content. It supports image-generation workflows as well as HTML-based graphics and PNG export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The PNG export helper may fetch an unpinned Playwright package and install it globally, then download Chromium.

Mitigation: Review the helper before running it; choose and pin the Playwright version and install it in an isolated project environment instead of relying on its automatic global install.

Risk: Sending a reference image to an external image-generation provider may disclose image contents.

Mitigation: Use only images you are authorized to share, and check the provider's data-handling terms before submitting sensitive material.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/bonniegeng-max/skills/style-card)
- [Reverse style analysis prompt](references/reverse-meta-prompt.md)
- [HTML template and rendering guidance](references/html-template.md)
- [HTML base stylesheet](references/html-base.css)
- [Generation gotchas](gotchas.md)
- [Frontend Slides, acknowledged workflow inspiration](https://github.com/zarazhangrui/frontend-slides)

## Skill Output:

**Output Type(s):** [Markdown, HTML, PNG images, Image-generation prompts, Guidance]

**Output Format:** [Reusable style cards and prompts in Markdown; optional single-file HTML and exported PNG graphics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Style cards use structured visual parameters and content slots; generated graphics depend on the selected image or HTML engine.]

## Skill Version(s):

0.6.5 (source: frontmatter, changelog released 2026-11-17)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
