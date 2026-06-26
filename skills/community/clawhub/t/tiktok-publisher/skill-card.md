## Description: <br>
Publish videos and photo carousels to TikTok with privacy settings and draft mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snoopyrain](https://clawhub.ai/user/snoopyrain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and social media operators use this skill to prepare and publish TikTok videos or photo carousels through Boring's MCP connector, including draft-mode review before a post goes live. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Boring MCP connector URL contains an embedded authentication token with delegated publishing authority for connected social accounts. <br>
Mitigation: Treat the connector URL like a password, share it only with trusted agents, and rotate or revoke it when access is no longer needed. <br>
Risk: The skill can create live TikTok posts through a third-party service. <br>
Mitigation: Require explicit user confirmation before publishing and use draft mode when review or approval is needed before a post goes live. <br>
Risk: Connected social accounts may grant broader posting capability than intended for a single task. <br>
Mitigation: Connect only the TikTok accounts intended for this workflow and disconnect or revoke access after use. <br>


## Reference(s): <br>
- [Boring MCP Connector Documentation](https://boring-doc.aiagent-me.com/getting-started/mcp.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/snoopyrain/tiktok-publisher) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration, Text] <br>
**Output Format:** [Markdown guidance with MCP tool call examples and status reporting] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Boring MCP connector URL containing an embedded authentication token.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
