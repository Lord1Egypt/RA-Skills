## Description: <br>
Track social media performance and analytics across connected Facebook, Instagram, Threads, YouTube, and TikTok accounts through the Boring MCP connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snoopyrain](https://clawhub.ai/user/snoopyrain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and social media teams use this skill to fetch and summarize account, post, video, publishing history, and cross-platform performance metrics from connected Boring accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP connector URL contains an embedded authentication token and functions like a credential. <br>
Mitigation: Treat the connector URL like a password, avoid sharing it, and revoke or regenerate it if exposed or no longer needed. <br>
Risk: The connector can access analytics and account metadata for connected social accounts. <br>
Mitigation: Install only when Boring is trusted for those accounts and confirm the connected permissions are read-only before use. <br>


## Reference(s): <br>
- [Boring MCP Connector Documentation](https://boring-doc.aiagent-me.com/getting-started/mcp.html) <br>
- [Boring Documentation](https://boring-doc.aiagent-me.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown summaries and tables with MCP tool calls as needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include account metrics, post rankings, trend summaries, cross-platform comparisons, and connector setup guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
