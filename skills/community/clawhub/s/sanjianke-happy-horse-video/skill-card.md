## Description:

Helps agents configure and use Happy Horse to submit and track short-video generation tasks from text or images through the a7w service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2253128](https://clawhub.ai/user/2253128)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to configure their own a7w API key, prepare text or image prompts, submit Happy Horse video tasks, and check results. Access to the video service requires an invitation during its testing period.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled client can store an a7w API key that also grants access to other a7w services.

Mitigation: Install only if you trust the a7w provider, protect the key, and rotate it if it may have been exposed.

Risk: Changing the client host can send the API key to an unintended destination.

Mitigation: Do not set a custom host unless you control and trust its destination; rotate the key if it was sent elsewhere.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/2253128/skills/sanjianke-happy-horse-video)
- [a7w API service](https://api.a7w.cn/)
- [Getting started and API key setup](references/getting-started.md)
- [Submit video task API](references/api-submit.md)
- [Create video task API](references/api-create.md)
- [Query video task API](references/api-query.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON task results]

**Output Format:** [Markdown instructions and command examples; JSON responses from API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video generation occurs through the external service; asynchronous tasks may return an ID before results are available.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata; bundled frontmatter says 1.0.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
