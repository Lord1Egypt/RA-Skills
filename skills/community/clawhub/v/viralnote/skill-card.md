## Description:

Schedule, publish, and manage social media content through the ViralNote API. Use when the user wants to post, schedule, query, or manage content across X, Facebook, Instagram, LinkedIn, TikTok, YouTube, Pinterest, Bluesky, Threads, or Reddit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[viralnote](https://clawhub.ai/user/viralnote)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to have an agent schedule posts, publish drafts, manage media, query analytics, and inspect connected social accounts through the ViralNote API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broad ViralNote API key could allow the agent to read, create, publish, delete, or manage more account content than the user intended.

Mitigation: Grant only the scopes needed for the workflow, keep VIRALNOTE_API_KEY in the environment, and never store the key in tracked files or chat logs.

Risk: Publishing immediately or deleting posts or media can affect live social accounts and may not be reversible.

Mitigation: Restate the platforms, caption, schedule time, and media, then wait for explicit user confirmation before immediate publishing or deletion.

Risk: Importing Dropbox, Canva, or signed media URLs sends those URLs to ViralNote's server.

Mitigation: Confirm that the URL is acceptable to share with ViralNote and that it serves the intended file directly before calling the import endpoint.

## Reference(s):

- [ViralNote Agents](https://www.viralnote.app/agents)
- [ViralNote API Reference](https://viralnote.app/developers/docs)
- [ViralNote OpenAPI Spec](https://viralnote.app/api/v1/openapi)
- [API Overview](reference/api-overview.md)
- [Authentication](reference/auth.md)
- [Schedule Post Workflow](examples/schedule-post.md)
- [Import Media Workflow](examples/import-media.md)
- [Analytics Workflow](examples/analytics.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown with inline bash commands and JSON request or response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a ViralNote API key supplied through VIRALNOTE_API_KEY; API responses are JSON.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
