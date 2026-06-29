## Description: <br>
Youtube Comment Manager helps agents list, search, reply to, update, delete, and moderate YouTube comment threads through AgentPMT-hosted tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, community managers, and agents use this skill to review YouTube comment threads, answer audience questions, search comments, and moderate held-for-review or likely-spam queues on connected channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Connected Google OAuth access can allow posting, deletion, moderation, and bans on YouTube comments. <br>
Mitigation: Install only if this access is acceptable for the connected channel, and keep tool inputs scoped to the comment-management task. <br>
Risk: Deleting comments, rejecting comments in bulk, posting replies, or banning authors can affect channel discussions; bans cannot be reversed from this tool. <br>
Mitigation: Use human review before destructive or bulk moderation actions, and reverse author bans through YouTube Studio when needed. <br>


## Reference(s): <br>
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/youtube-comment-manager) <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/youtube-comment-manager) <br>
- [Generated action schema](artifact/schema.md) <br>
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration] <br>
**Output Format:** [Markdown instructions with JSON call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote tool responses are JSON wrappers around YouTube comment, thread, and moderation payloads.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
