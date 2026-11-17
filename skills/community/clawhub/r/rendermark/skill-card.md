## Description:

Turns Markdown into styled previews, exported documents, images, and shareable published pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jmsaavedra](https://clawhub.ai/user/jmsaavedra)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and documentation teams use RenderMark to preview, export, compare, validate, and publish Markdown documents or sync them from GitHub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sharing and GitHub imports can publish documents without first establishing who should have access.

Mitigation: For sensitive documents, confirm the hosting destination and audience and set access restrictions before publication; request local export when hosting is unnecessary, and disable immediate publication for GitHub imports.

Risk: The external server’s implementation and access controls remain unverified.

Mitigation: Pin a reviewed server version and protect its credential file.

## Reference(s):

- [Setup guide](references/setup-guide.md)
- [Tools reference](references/tools-reference.md)
- [RenderMark website](https://rendermark.app)
- [RenderMark MCP Server on npm](https://www.npmjs.com/package/@rendermark/mcp-server)
- [ClawHub release](https://clawhub.ai/jmsaavedra/skills/rendermark)

## Skill Output:

**Output Type(s):** [HTML, PDF, DOCX, PNG/JPEG images, Google Docs, Shareable document links]

**Output Format:** [Styled previews, exported document files, image data, or hosted document links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output format, theme, template, and sharing options vary by requested tool.]

## Skill Version(s):

0.1.12 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
