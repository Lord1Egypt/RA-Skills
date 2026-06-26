## Description: <br>
Tracks YouTube channel performance and analytics, including views, watch time, subscriber growth, engagement, and per-video metrics through a Boring MCP connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snoopyrain](https://clawhub.ai/user/snoopyrain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, channel operators, and agents use this skill to answer YouTube analytics questions, compare channel and video performance, and summarize trends from connected read-only analytics data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP connector URL contains an embedded authentication token that can grant read-only access to YouTube analytics if exposed. <br>
Mitigation: Treat the connector URL like a password, avoid sharing it publicly, and revoke or regenerate it in Boring settings if it is exposed. <br>
Risk: The skill depends on a third-party Boring service to retrieve analytics data. <br>
Mitigation: Install only if you trust Boring with read-only YouTube analytics access and review the connected account before use. <br>


## Reference(s): <br>
- [Youtube Performance on ClawHub](https://clawhub.ai/snoopyrain/youtube-performance) <br>
- [Boring MCP connector documentation](https://boring-doc.aiagent-me.com/getting-started/mcp.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summaries, tables, and tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses read-only analytics data returned through the configured Boring MCP connector.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
