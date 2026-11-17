## Description:

Helps agents submit and track text-to-image and image-editing tasks through the a7w nano_banana plugin using a user-provided API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2253128](https://clawhub.ai/user/2253128)

### License/Terms of Use:

MIT

## Use Case:

Creators and developers use this skill to generate or edit images, choose model and image options, and check asynchronous task results through a7w.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API key can access other a7w plugins beyond nano_banana.

Mitigation: Use a scoped or low-balance key if available and review which account permissions the client can exercise.

Risk: Prompts and input image URLs are sent to the external image service.

Mitigation: Avoid sensitive prompts and private image URLs.

Risk: A custom host or insecure callback could expose credentials or results.

Mitigation: Keep the default host unless you trust the destination, and use HTTPS authenticated callbacks.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/2253128/skills/sanjianke-nano-banana-image)
- [a7w API and key setup](https://api.a7w.cn/)
- [Getting started](references/getting-started.md)
- [Submit image task API](references/api-submit.md)
- [Query image task API](references/api-query.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Text guidance and JSON task results containing task IDs, status, and image URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image results are returned as URLs; asynchronous tasks may require polling.]

## Skill Version(s):

1.0.7 (source: server-resolved ClawHub release; bundled frontmatter lists 1.0.6)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
