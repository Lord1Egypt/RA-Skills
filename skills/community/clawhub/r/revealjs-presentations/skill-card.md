## Description:

Create, edit, and deploy reveal.js presentations as single HTML files with optional custom CSS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielgrobelny](https://clawhub.ai/user/danielgrobelny)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and other presentation authors use this skill to create web-based slide decks, pitch decks, talks, and deployable reveal.js presentations as static HTML.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CDN-hosted reveal.js dependencies may be unsuitable for sensitive, offline, or long-lived hosted presentations.

Mitigation: Review the CDN dependency choice before deployment; pin exact reveal.js versions, add subresource integrity, or vendor reveal.js locally when needed.

Risk: Generated decks may retain the template's default English HTML language attribute even when the presentation is not in English.

Mitigation: Set the HTML lang attribute to match the deck language before publishing.

## Reference(s):

- [reveal.js API Reference](references/revealjs-api.md)
- [ClawHub skill page](https://clawhub.ai/danielgrobelny/skills/revealjs-presentations)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration, Shell commands]

**Output Format:** [Markdown guidance with HTML, CSS, and JavaScript snippets; generated deck output is a single static HTML file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses reveal.js v5 via CDN by default and can include custom CSS, plugins, speaker notes, fragments, backgrounds, and static deployment instructions.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
