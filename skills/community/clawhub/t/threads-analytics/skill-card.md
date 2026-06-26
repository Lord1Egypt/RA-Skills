## Description: <br>
Track Threads performance and analytics, including views, likes, replies, reposts, follower counts, and engagement data for a connected Threads account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snoopyrain](https://clawhub.ai/user/snoopyrain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, creators, and social media teams use this skill to query read-only Threads analytics through a Boring MCP connector and summarize account, post, and historical performance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP connector URL contains an embedded authentication token that may allow access to connected Threads analytics if shared. <br>
Mitigation: Keep the connector URL private, install only if you trust Boring with read-only analytics access, and revoke or regenerate the URL if it may have been exposed. <br>
Risk: The skill relies on a third-party MCP service to retrieve account and performance metrics. <br>
Mitigation: Connect only accounts whose read-only metrics can be shared with that service and review the returned analytics before acting on them. <br>


## Reference(s): <br>
- [Threads Analytics on ClawHub](https://clawhub.ai/snoopyrain/threads-analytics) <br>
- [Boring MCP Connector Documentation](https://boring-doc.aiagent-me.com/getting-started/mcp.html) <br>
- [Boring Documentation](https://boring-doc.aiagent-me.com) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown summaries and tables based on MCP tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a user-configured read-only MCP connector for Threads analytics.] <br>

## Skill Version(s): <br>
1.0.1 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
