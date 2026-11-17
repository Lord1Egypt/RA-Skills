## Description:

Converts Markdown articles into pure inline-styled HTML that can be pasted into the WeChat Official Account editor, covering headings, paragraphs, lists, bold text, inline code, tables, blockquotes, code blocks, and images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerryaction](https://clawhub.ai/user/jerryaction)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content authors, and developers use this skill to convert Markdown source articles into WeChat-compatible HTML files for direct copy-paste into WeChat drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML may carry unsafe or misleading content when the source Markdown, image URLs, or embedded HTML come from untrusted parties.

Mitigation: Review and sanitize generated HTML before opening it in a browser or pasting it into WeChat or other publishing systems.

Risk: The skill writes local HTML files derived from user-provided Markdown.

Mitigation: Run it only on Markdown sources you intend to convert and inspect the output file before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jerryaction/skills/wechat-article-html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Guidance]

**Output Format:** [Inline-styled HTML file and concise conversion guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces UTF-8 HTML intended for WeChat editor paste workflows; generated HTML should be reviewed or sanitized when source content is untrusted.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
