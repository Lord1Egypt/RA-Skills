## Description:

Drive PurrPlan, a social media scheduler, from an agent to plan, draft, schedule and publish posts across 12+ networks, manage the unified inbox, and read analytics through PurrPlan's remote MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sebastiendb](https://clawhub.ai/user/sebastiendb)

### License/Terms of Use:

MIT-0

## Use Case:

External users and social media teams use this skill to connect an agent to PurrPlan for content planning, drafting, scheduling, publishing, inbox handling, and social analytics. The skill is most appropriate when the user wants agent-assisted social media operations with explicit approval before publishing posts or sending inbox replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback setup uses an unpinned npm bridge for MCP clients without native HTTP support.

Mitigation: Prefer native HTTP MCP configuration; if a bridge is required, use a pinned and reviewed bridge version.

Risk: Bearer tokens can be exposed when placed directly in shell commands.

Mitigation: Store tokens in a protected secret mechanism, grant minimum scopes, avoid production tokens in command lines, and rotate or revoke exposed tokens.

Risk: Publishing posts or replying to inbox messages can act on real social accounts.

Mitigation: Require explicit user approval in the conversation, show draft content first, and set confirmation flags only after approval.

## Reference(s):

- [PurrPlan ClawHub Skill Page](https://clawhub.ai/sebastiendb/skills/purrplan)
- [PurrPlan Developer Documentation](https://purrplan.ai/en/developpeurs)
- [PurrPlan MCP Integration](https://app.purrplan.ai/app/mcp-integration)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands]

**Output Format:** [Markdown with JSON MCP configuration and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes workflow guidance for MCP tool calls, approval gates for publishing and inbox replies, and rate-limit handling.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
