## Description:

Generates professional Chinese visual note cards and poster-style infographics as self-contained HTML files with optional automatic PNG export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tom859174-sketch](https://clawhub.ai/user/tom859174-sketch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to convert topics, articles, or concepts into structured Chinese visual note cards for social sharing, presentations, or printing. The skill guides the agent to produce a complete HTML infographic and, by default, export it as a PNG image.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated cards may load Google Fonts and CDN JavaScript.

Mitigation: Review generated HTML and vendor or pin external assets before routine use.

Risk: The PNG exporter opens active HTML in Chromium with no-sandbox flags.

Mitigation: Run exports in a restricted environment without sensitive files or credentials, and remove no-sandbox flags where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tom859174-sketch/skills/visual-note-card)
- [README](artifact/README.md)
- [Reference HTML template](artifact/assets/template.html)
- [PNG export script](artifact/scripts/html2png.py)

## Skill Output:

**Output Type(s):** [Code, Files, Shell commands, Guidance]

**Output Format:** [Self-contained HTML, PNG image, and concise Markdown delivery notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated HTML may load Google Fonts and html2canvas from third-party CDNs; PNG export uses a Playwright-based Chromium screenshot workflow.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
