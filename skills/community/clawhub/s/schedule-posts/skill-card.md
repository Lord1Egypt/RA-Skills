## Description:

Schedules and manages single, bulk, next-slot, and recurring social media posts through PostWire, with network-specific checks before queueing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perufitlife](https://clawhub.ai/user/perufitlife)

### License/Terms of Use:

MIT-0

## Use Case:

Social media managers and other users schedule, review, and manage posts across connected social networks through PostWire, including batches from CSV files and recurring posts where their plan permits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting social accounts gives PostWire access to those accounts.

Mitigation: Connect accounts only if comfortable granting PostWire that access.

Risk: Incorrect post text, target networks, or scheduling times could publish unintended content.

Mitigation: Review each post, its networks, and its local scheduled time before confirming; dry-run batches before queueing.

Risk: Remote PostWire setup instructions could change before the MCP server is added.

Mitigation: Inspect the remote setup instructions before adding the server.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/perufitlife/skills/schedule-posts)
- [PostWire](https://postwire.io/)
- [PostWire setup instructions](https://postwire.io/SKILL.md)
- [PostWire error codes](https://postwire.io/docs/errors.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Post previews, scheduled times and networks, validation warnings, and queue summaries.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
