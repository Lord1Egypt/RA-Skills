## Description:

Youtube Comment Manager helps agents list, search, reply to, edit, delete, and moderate YouTube comments through AgentPMT-hosted remote tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, community managers, and agents use this skill to triage YouTube comments, respond to viewer questions, search discussion threads, and moderate held-for-review or likely-spam queues on connected channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can post replies, delete comments, reject comments, bulk moderate queues, and ban authors for the connected Google account.

Mitigation: Require explicit approval before write, delete, reject, bulk moderation, or ban_author actions, and keep requested operations scoped to the minimum necessary comments.

Risk: The release evidence reports mutable setup and live-instruction paths that users should review carefully.

Mitigation: Prefer pinned or reviewed setup-skill versions and review live schemas or instructions before using the skill in production workflows.

## Reference(s):

- [Generated action schema](artifact/schema.md)
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/youtube-comment-manager)
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/youtube-comment-manager)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)

## Skill Output:

**Output Type(s):** [guidance, API Calls, JSON, configuration]

**Output Format:** [Markdown guidance with JSON tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs describe AgentPMT-hosted YouTube comment actions and response handling; tool responses wrap YouTube Data API payloads as JSON.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
