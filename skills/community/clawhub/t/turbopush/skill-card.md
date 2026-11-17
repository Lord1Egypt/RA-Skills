## Description:

Multi-platform content publishing assistant that helps agents publish articles, image posts, and videos to 20+ platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyc1f](https://clawhub.ai/user/xueyc1f)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content operators use this skill to guide an agent through preparing and publishing content across logged-in social and media accounts. It is suited for coordinated article, image-post, and video publishing workflows that require account checks, platform settings, result confirmation, and browser cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connected tool can publish through logged-in social and media accounts.

Mitigation: Review target accounts and post content before publishing, and use draft or sync options where available for preview.

Risk: The skill depends on a local TurboPush MCP binary and authenticated local service.

Mitigation: Install only from a trusted TurboPush MCP source and keep TURBO_PUSH_AUTH scoped to the local service.

Risk: Browser instances can remain open after publishing workflows.

Mitigation: Use closeBrowser=true for publishing calls or run close_browser after completing publishing tasks.

## Reference(s):

- [TurboPush ClawHub listing](https://clawhub.ai/xueyc1f/skills/turbopush)
- [TurboPush MCP repository](https://github.com/xueyc/turbopush-mcp)
- [TurboPush MCP releases](https://github.com/xueyc/turbopush-mcp/releases)
- [TurboPush application repository](https://github.com/xueyc/turbopush)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code, command examples, and structured publishing parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides calls to a local TurboPush MCP server and may produce platform-specific settings for publishing workflows.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
