## Description:

Helps agents create, edit, and check Wan video-generation tasks through the a7w API using a user-provided API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2253128](https://clawhub.ai/user/2253128)

### License/Terms of Use:

MIT

## Use Case:

Creators and developers use this skill to submit text-to-video, reference-image-to-video, and video-editing tasks, then check task status and retrieve video links. An a7w account and API key are required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, media URLs, callback URLs, and API credentials are shared with the a7w service.

Mitigation: Use only if you trust api.a7w.cn and the publisher; avoid sending sensitive material and protect or revoke exposed keys.

Risk: A custom server address can receive a saved API key.

Mitigation: Do not set --host or A7W_HOST unless the destination is trusted.

Risk: The bundled client can access marketplace APIs beyond Wan, and generation may consume paid credits.

Mitigation: Limit agent access to Wan create/query operations and review account usage before submitting tasks.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/2253128/skills/sanjianke-wan-video)
- [Publisher profile](https://clawhub.ai/user/2253128)
- [Getting started](references/getting-started.md)
- [Create video task API](references/api-create.md)
- [Query video task API](references/api-query.md)
- [a7w API and account](https://api.a7w.cn/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, JSON responses, Guidance]

**Output Format:** [Markdown guidance and shell commands; API responses as JSON with task status and video URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task creation is asynchronous; completed results include a video URL. Generated videos are delivered through the API, not embedded in the agent response.]

## Skill Version(s):

1.0.7 (source: ClawHub release metadata; artifact frontmatter lists 1.0.6)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
