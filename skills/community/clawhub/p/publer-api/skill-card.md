## Description:

Use this skill when an agent needs to interact with the Publer API to manage social media posts, media, workspaces, connected accounts, analytics, competitors, or hashtag performance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gjeka](https://clawhub.ai/user/gjeka)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and social media teams use this skill to let an agent schedule, publish, update, delete, and review Publer-managed posts; upload media; retrieve analytics; and inspect competitor or hashtag performance through Publer's API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through sensitive publishing, update, and deletion operations using a Publer API key.

Mitigation: Use the minimum required API scopes, keep API keys private, and require preview and confirmation of exact accounts, content, schedule times, and post IDs before publishing, updating, or deleting posts.

Risk: Asynchronous Publer operations can complete with partial failures.

Mitigation: Poll job status until completion and review failure payloads before reporting a post, media upload, or publishing workflow as successful.

## Reference(s):

- [Publer API Reference](api-reference.md)
- [Publer API Base URL](https://app.publer.com/api/v1)
- [ClawHub Skill Page](https://clawhub.ai/gjeka/skills/publer-api)
- [Publisher Profile](https://clawhub.ai/user/gjeka)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided Publer API key and workspace context; publishing and deletion actions should be previewed and confirmed before execution.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
