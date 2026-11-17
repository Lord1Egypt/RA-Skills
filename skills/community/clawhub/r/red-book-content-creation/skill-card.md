## Description:

Converts articles, technical documents, and other text into Xiaohongshu-ready HTML pages with a title, summary, cover, and screenshot-ready visual content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenhulove333](https://clawhub.ai/user/wenhulove333)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and developers use this skill to turn Markdown or plain text into Xiaohongshu-style visual posts for technical explainers, product introductions, marketing content, and knowledge sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided text is inserted into generated HTML by the local shell generator without safe escaping.

Mitigation: Review generated HTML before rendering, avoid untrusted or sensitive input, and replace shell placeholder substitution with safe escaping before deployment.

Risk: Rendering generated HTML can execute template scripts and load KaTeX assets from a CDN.

Mitigation: Render in a sandboxed environment and document or restrict network access for CDN-loaded assets.

Risk: Generated HTML and PNG outputs may retain user content on disk.

Mitigation: Define output retention and cleanup practices before using the skill with confidential material.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wenhulove333/skills/red-book-content-creation)
- [KaTeX stylesheet CDN](https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css)
- [KaTeX script CDN](https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, files, guidance]

**Output Format:** [Markdown guidance with generated HTML, shell commands, and PNG/HTML output file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses 680px-wide HTML templates and screenshot generation for Xiaohongshu-style image posts.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
