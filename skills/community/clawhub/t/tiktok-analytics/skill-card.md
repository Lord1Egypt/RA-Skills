## Description: <br>
Track TikTok account and video performance, including views, likes, comments, shares, engagement, and publishing history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snoopyrain](https://clawhub.ai/user/snoopyrain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and social media operators use this skill to query TikTok account-level and per-video analytics through the Boring MCP connector and present the results as summaries, ranked videos, and trend reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP connector link contains an embedded authentication token. <br>
Mitigation: Treat the connector link like a password, avoid sharing it publicly, and revoke or regenerate it if exposed. <br>
Risk: The skill depends on a third-party connector to access TikTok analytics. <br>
Mitigation: Install only if you are comfortable connecting TikTok analytics through Boring and confirm the connector remains read-only before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/snoopyrain/tiktok-analytics) <br>
- [Boring MCP Documentation](https://boring-doc.aiagent-me.com/getting-started/mcp.html) <br>
- [Boring Documentation](https://boring-doc.aiagent-me.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown summaries, tables, and MCP tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on the connected TikTok account, Boring MCP connector availability, and the connector's read-only analytics scope.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
