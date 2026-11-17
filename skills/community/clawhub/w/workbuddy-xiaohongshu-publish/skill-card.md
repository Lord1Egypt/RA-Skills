## Description:

Xiaohongshu Publish helps agents turn Markdown or HTML notes into Xiaohongshu image posts and publish them through a macOS local Chrome workflow after user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a-persimmons](https://clawhub.ai/user/a-persimmons)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and content teams use this skill to prepare Xiaohongshu image posts from Markdown or HTML content, preview the generated cards, and publish through a local browser-backed workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and run an unverified third-party binary.

Mitigation: Install only from trusted release sources, verify a pinned checksum or build from reviewed source, and use a dedicated working directory.

Risk: The workflow can access Xiaohongshu account cookies and publish public posts.

Mitigation: Protect cookies.json, preview every generated post, and require explicit user confirmation before publishing.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/a-persimmons/workbuddy-xiaohongshu-publish)
- [Xiaohongshu MCP releases](https://github.com/xpzouying/xiaohongshu-mcp/releases)
- [ClawHub skill page](https://clawhub.ai/a-persimmons/skills/workbuddy-xiaohongshu-publish)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, markdown]

**Output Format:** [Markdown guidance with shell command examples and workflow constraints]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent instructions for rendering image-post assets, managing login cookies, starting a local MCP service, previewing outputs, and publishing only after user confirmation.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
