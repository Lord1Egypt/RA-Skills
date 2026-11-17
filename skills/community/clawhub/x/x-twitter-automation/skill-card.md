## Description:

Helps agents search, publish, engage, and manage direct messages through a connected X account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Social media teams and developers use this skill to monitor X conversations, publish posts and replies, manage engagement, and respond to customer messages from agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connected account access can expose private DMs and enable public posts, replies, follows, reposts, and deletions.

Mitigation: Limit account permissions where possible and require human approval before sending messages or changing public account state.

Risk: Engagement actions may be used to unlock unsolicited replies.

Mitigation: Do not like or repost solely to qualify an unsolicited reply.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/agentpmt/skills/x-twitter-automation)
- [AgentPMT marketplace listing](https://www.agentpmt.com/marketplace/x-twitter-automation)
- [Action schema](artifact/schema.md)

## Skill Output:

**Output Type(s):** [Guidance, JSON]

**Output Format:** [Markdown instructions and structured action results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected X account and requested action.]

## Skill Version(s):

1.0.1 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
