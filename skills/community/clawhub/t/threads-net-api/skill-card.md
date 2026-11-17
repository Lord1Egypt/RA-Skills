## Description:

Guides agents in retrieving public Threads profiles, posts, replies, comment threads, and matching accounts through Scavio's API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to research public Threads accounts and retrieve profiles, posts, replies, and comments, or find accounts by name or handle.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Threads identifiers and search queries are sent to Scavio as an intermediary.

Mitigation: Use only if that data flow is acceptable, and avoid putting private or sensitive notes in search queries.

Risk: Calls require a Scavio API key and consume paid credits after any available free allowance.

Mitigation: Supply the key through the environment, keep it out of shared output, and monitor credit use; reuse user IDs to avoid higher-cost username lookups.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/scavio-ai/skills/threads-net-api)
- [Scavio Threads profile API documentation](https://scavio.dev/docs/threads-profile?utm_source=agent-skills&utm_medium=skill&utm_campaign=threads-net-api)
- [Scavio Threads posts API documentation](https://scavio.dev/docs/threads-user-posts?utm_source=agent-skills&utm_medium=skill&utm_campaign=threads-net-api)
- [Scavio Threads replies API documentation](https://scavio.dev/docs/threads-user-replies?utm_source=agent-skills&utm_medium=skill&utm_campaign=threads-net-api)
- [Scavio Threads post and comments API documentation](https://scavio.dev/docs/threads-post-comments?utm_source=agent-skills&utm_medium=skill&utm_campaign=threads-net-api)
- [Scavio Threads people search API documentation](https://scavio.dev/docs/threads-user-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=threads-net-api)

## Skill Output:

**Output Type(s):** [Text, JSON, Code, Shell commands, Guidance]

**Output Format:** [Text or Markdown with structured JSON results and example API requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public Threads data only; account search does not search post content. Some results are cursor-paginated.]

## Skill Version(s):

1.0.4 (source: server-resolved release; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
