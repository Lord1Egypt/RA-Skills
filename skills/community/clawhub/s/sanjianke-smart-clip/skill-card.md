## Description:

Helps agents find video templates and create talking-head, material-mix, and news-style videos through the A7W smart-clip service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2253128](https://clawhub.ai/user/2253128)

### License/Terms of Use:

MIT

## Use Case:

Creators and developers use this skill to query editing templates and submit video-editing jobs using their own A7W API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled client can use the API key to call A7W plugins beyond smart-clip.

Mitigation: Review commands and use only an A7W key whose permitted access and usage you accept.

Risk: Changing the service host could send the API key to an untrusted destination.

Mitigation: Avoid custom --host or A7W_HOST settings unless you trust the destination.

Risk: Media and callback URLs, task data, and generated results are processed by an external service.

Mitigation: Share only approved media and URLs; review destination and data-handling requirements before submitting jobs.

Risk: The API key may be saved on the local device.

Mitigation: Protect locally stored credentials and avoid using a key you are uncomfortable storing there.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/2253128/skills/sanjianke-smart-clip)
- [A7W API and account setup](https://api.a7w.cn/)
- [Getting started](references/getting-started.md)
- [Smart-clip API reference](references/api-template.md)
- [Video editing API reference](references/api-broadcast_mixcut.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown instructions and commands; JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Async editing tasks may return a generated video URL after polling.]

## Skill Version(s):

1.0.5 (source: server-resolved release; bundled frontmatter lists 1.0.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
