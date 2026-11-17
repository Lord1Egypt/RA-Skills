## Description:

Create polished, editable SVG cover artwork for reports, articles, slide decks, social cards, ebook covers, posters, and landing-page hero images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nimachu](https://clawhub.ai/user/nimachu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and content teams use this skill to generate editable, self-contained SVG cover artwork for reports, slide decks, social cards, posters, ebooks, and hero images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SVG files from untrusted sources can contain unsafe constructs, and the included validator is not a complete SVG security sanitizer.

Mitigation: Review SVG content before opening or distributing it; use the bundled validator as a structural check and apply trusted SVG sanitization where security boundaries matter.

## Reference(s):

- [SVG Cover Design Rules](references/design-rules.md)
- [Layout Recipes](references/layout-recipes.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Files, Shell commands, Guidance]

**Output Format:** [Markdown with fenced SVG code blocks or generated SVG files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Self-contained SVG with editable text and no external dependencies; optional structural validation with scripts/check_svg.py.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
