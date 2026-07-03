## Description: <br>
Operates a connected X/Twitter account through AgentPMT so agents can publish posts and replies, search recent posts, manage engagement, work with Lists, upload media, and handle DMs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, social media teams, and developers use this skill to let an agent operate an AgentPMT-connected X/Twitter account for publishing, monitoring, engagement, Lists, media uploads, and DM workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can read DMs and take public or destructive account actions, including posting, deleting, following, unfollowing, liking, reposting, hiding replies, uploading media, and sending DMs. <br>
Mitigation: Require explicit approval before those actions, restrict workflows to intended accounts and tasks, and keep connected account scopes as narrow as possible. <br>
Risk: Prompts or logs may expose account secrets, payment headers, or sensitive DM content. <br>
Mitigation: Do not place secrets or sensitive DM content in prompts or logs; use setup skills for credential handling and pass only the minimum content needed for each task. <br>
Risk: Uploading media from URLs can cause externally fetched content to be published or sent from the connected account. <br>
Mitigation: Ask before URL-based uploads and verify the media source and intended post or DM context before using the returned media ID. <br>


## Reference(s): <br>
- [AgentPMT Marketplace: X Twitter Automation](https://www.agentpmt.com/marketplace/x-twitter-automation) <br>
- [ClawHub: X Twitter Automation](https://clawhub.ai/agentpmt/skills/x-twitter-automation) <br>
- [Action Schema](artifact/schema.md) <br>
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>
- [What Is AgentPMT](https://clawhub.ai/agentpmt/what-is-agentpmt) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown instructions with JSON tool-call examples and JSON response handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defines 26 AgentPMT-hosted X/Twitter actions; responses return an action field, and some responses include data, includes, meta, and pagination tokens.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
