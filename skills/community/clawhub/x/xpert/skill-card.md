## Description: <br>
Grow on X (Twitter) with Xpert by connecting over MCP or REST to draft, rewrite, schedule, analyze, and reply in the user's own voice using OAuth 2.1 with dynamic client registration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xpert](https://clawhub.ai/user/xpert) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to Xpert so it can help manage X/Twitter growth workflows, including post drafting, rewriting, scheduling, analytics review, trend research, and audience replies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can request broad X/Twitter account powers, including publishing, engagement automation, direct-message outreach, and account or API-key management. <br>
Mitigation: Grant only the OAuth scopes needed for the current workflow and avoid admin or direct-message access unless those features are specifically required. <br>
Risk: Generated posts, replies, schedules, or outreach could be published or acted on in ways the user did not intend. <br>
Mitigation: Review generated content and planned actions with the user before publishing, scheduling, replying, or starting outreach. <br>
Risk: AI actions are credit-metered, so repeated generation or analysis can consume paid credits. <br>
Mitigation: Check the user's available balance or billing surface when calls fail with insufficient credits and keep generation loops bounded. <br>


## Reference(s): <br>
- [Xpert homepage](https://xpert.so) <br>
- [ClawHub skill page](https://clawhub.ai/xpert/xpert) <br>
- [MCP server card](https://xpert.so/.well-known/mcp/server-card.json) <br>
- [OAuth authorization server metadata](https://api.xpert.so/.well-known/oauth-authorization-server) <br>
- [MCP protected resource metadata](https://mcp.xpert.so/.well-known/oauth-protected-resource) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown guidance with OAuth flow details, MCP tool usage, REST endpoint references, and generated social-content text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated content should be reviewed before publishing; OAuth scopes should be limited to the required workflow.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
