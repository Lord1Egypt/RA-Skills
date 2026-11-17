## Description:

Publish videos and photo carousels to TikTok with privacy settings and draft mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snoopyrain](https://clawhub.ai/user/snoopyrain)

### License/Terms of Use:

MIT-0

## Use Case:

External users and social media operators use this skill to publish TikTok videos or photo carousels through the Boring MCP connector, including draft-mode review before a post goes live.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP connector URL contains an embedded bearer token with authority to publish to connected social accounts.

Mitigation: Treat the connector URL like a password, avoid sharing it, and revoke or regenerate the token if it is exposed.

Risk: The connector can publish public TikTok content through connected accounts.

Mitigation: Confirm the connected TikTok account before use and prefer draft mode when review is needed before posting.

Risk: The release evidence flags inconsistent data-flow descriptions.

Mitigation: Review the documented data handling and connected-service permissions before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/snoopyrain/skills/tiktok-publisher)
- [Boring MCP Connector Documentation](https://boring-doc.aiagent-me.com/getting-started/mcp.html)

## Skill Output:

**Output Type(s):** [guidance, API Calls, configuration, text]

**Output Format:** [Markdown guidance with MCP tool-call examples and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports post ID and success status; draft posts require final publishing in the TikTok app.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
