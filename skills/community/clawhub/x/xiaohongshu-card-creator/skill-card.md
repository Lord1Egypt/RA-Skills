## Description:

Xiaohongshu Card Creator converts Markdown copy into Xiaohongshu-style HTML card pages, with template and optional LLM-assisted modes for exporting vertical PNG cards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[riverfor](https://clawhub.ai/user/riverfor)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and developers use this skill to turn Markdown drafts into 3:4 Xiaohongshu-style card pages and downloadable PNG images for review and publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated cards may include unsafe HTML or injected browser code.

Mitigation: Review and sanitize generated HTML before broad use or publication, and avoid running the skill on untrusted Markdown.

Risk: Optional LLM mode can expose private drafts or API credentials to the configured endpoint.

Mitigation: Use LLM mode only with trusted endpoints and non-sensitive drafts, and protect LLM_API_KEY and .env files.

Risk: Generated visual cards may be inaccurate or unsuitable for publication without review.

Mitigation: Review generated cards before publishing.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/riverfor/skills/xiaohongshu-card-creator)
- [html2canvas 1.4.1 CDN dependency](https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js)

## Skill Output:

**Output Type(s):** [Files, HTML, PNG images, Shell commands, Configuration]

**Output Format:** [Generated HTML page with downloadable PNG card images]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates 1-20 vertical 3:4 cards and supports optional LLM-assisted HTML generation when configured.]

## Skill Version(s):

1.4.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
