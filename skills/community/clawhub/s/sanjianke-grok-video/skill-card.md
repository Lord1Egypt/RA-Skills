## Description:

Helps agents submit Grok video-generation tasks and check their results through a7w using a user-provided API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2253128](https://clawhub.ai/user/2253128)

### License/Terms of Use:

MIT

## Use Case:

Creators and developers use this skill to submit text prompts or reference images for video generation, then check task status and retrieve video links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The same API key can access other a7w marketplace apps beyond video generation.

Mitigation: Review the skill before installation, limit use to grok_video submit/query, and monitor account activity and charges.

Risk: A custom host can receive the API key if it points to an untrusted server.

Mitigation: Avoid untrusted --host or A7W_HOST values and use the expected a7w endpoint.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/2253128/skills/sanjianke-grok-video)
- [Getting started](artifact/references/getting-started.md)
- [Submit video task API](artifact/references/api-submit.md)
- [Query video task API](artifact/references/api-query.md)
- [a7w API platform](https://api.a7w.cn/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown instructions and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task submissions return IDs; completed queries can return video URLs.]

## Skill Version(s):

1.0.7 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
