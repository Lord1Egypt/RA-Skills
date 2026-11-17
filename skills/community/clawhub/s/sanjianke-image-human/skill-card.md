## Description:

Guides an agent in creating talking-avatar videos from a person’s photo and a voice recording through the a7w image_human service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2253128](https://clawhub.ai/user/2253128)

### License/Terms of Use:

MIT

## Use Case:

Content creators and marketing teams use this skill to submit a photo and voice recording for a talking-avatar video, then check the generation result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A person’s face and voice material is sent to an external video-generation service, creating privacy and impersonation risks.

Mitigation: Obtain consent for the likeness and voice, and submit only material approved for the service.

Risk: The paid API key can access services beyond video generation, and a custom host can receive the key.

Mitigation: Use temporary environment credentials, keep the default api.a7w.cn host, and limit agent calls to image_human submit and query.

Risk: Submitting tasks consumes account credits, and repeat submissions can generate additional charges.

Mitigation: Confirm the resolution tier and cost before submission; query the existing task rather than resubmitting it.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/2253128/skills/sanjianke-image-human)
- [Getting started](references/getting-started.md)
- [Submit API reference](references/api-submit.md)
- [Query API reference](references/api-query.md)
- [a7w API service](https://api.a7w.cn/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance, shell commands, and JSON task results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task results may include a generated-video URL; creation requires a user-supplied API key and may incur charges.]

## Skill Version(s):

1.1.1 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
