## Description:

Toutiao Mcp helps agents manage a Toutiao account and publish articles, micro posts, and batch Xiaohongshu-derived content through the toutiao-mcp MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sipingme](https://clawhub.ai/user/sipingme)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, publishers, and operators use this skill to let an agent check Toutiao login status, guide login, publish articles or micro posts, and batch-post Xiaohongshu-formatted content to Toutiao.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned or unreviewed MCP server installation could run code the user did not intend to trust.

Mitigation: Install toutiao-mcp only from a trusted, pinned version or reviewed commit, and avoid sudo npm install.

Risk: Saved Toutiao cookies can grant account access if exposed from the local cookie file.

Mitigation: Store the cookie file in a user-controlled local path with restricted permissions and remove or rotate it when access should end.

Risk: Publishing and batch publishing affect a real public Toutiao account.

Mitigation: Confirm content, images, tags, and batch inputs carefully before calling publishing tools.

## Reference(s):

- [Toutiao Mcp on ClawHub](https://clawhub.ai/sipingme/skills/toutiao-mcp-skill)
- [Quick Start](references/quick-start.md)
- [FAQ](references/faq.md)
- [Troubleshooting](references/troubleshooting.md)
- [toutiao-mcp-skill repository](https://github.com/sipingme/toutiao-mcp-skill)
- [toutiao-mcp MCP server](https://github.com/sipingme/toutiao-mcp)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, JSON]

**Output Format:** [Markdown guidance with shell commands, MCP configuration snippets, and JSON tool inputs or responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include live publishing confirmations, article or post IDs, URLs, and batch publishing summaries.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
