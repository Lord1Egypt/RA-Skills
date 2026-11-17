## Description:

Uses the Model Context Protocol to help an agent operate Xiaohongshu for publishing, search, recommendations, comments, likes, favorites, and login checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sipingme](https://clawhub.ai/user/sipingme)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to configure an agent to operate a Xiaohongshu account through an MCP server for content publishing, content search, recommendations, and engagement actions after login confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The quick-start path recommends a remote shell installer, and the security evidence calls out installer review needs.

Mitigation: Review the installer first or use manual, pinned installation steps instead of piping a remote script to bash.

Risk: The skill automates real Xiaohongshu account actions and relies on a local cookie file.

Mitigation: Treat the cookie file as a login credential, keep it private, and require explicit preview and confirmation before publish, comment, like, or favorite actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sipingme/skills/xiaohongshu-mcp-node-skill)
- [Quick Start Guide](artifact/references/quick-start.md)
- [FAQ](artifact/references/faq.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON examples, and MCP action descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command and tool results are typically JSON; account-changing actions should be previewed and confirmed before execution.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
