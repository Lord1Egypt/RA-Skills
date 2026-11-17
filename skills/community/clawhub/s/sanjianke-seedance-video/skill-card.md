## Description:

Helps agents create multimodal Seedance 2.0 video tasks and manage media assets through the a7w API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2253128](https://clawhub.ai/user/2253128)

### License/Terms of Use:

MIT

## Use Case:

Creators and developers use the skill to submit text, image, video, or audio inputs for Seedance video generation and manage related assets and task results. An a7w API key is required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled client can use the same API key to enumerate and call a7w marketplace plugins beyond Seedance.

Mitigation: Review this broader access before installation and use a least-privilege a7w API key where available.

Risk: A custom API host could receive the API key and submitted data.

Mitigation: Do not set --host or A7W_HOST unless you trust the endpoint.

Risk: Deleting an asset with the wrong ID can remove unintended media.

Mitigation: Confirm asset IDs before deletion.

Risk: Web search or callback URLs may expose sensitive prompts or media URLs.

Mitigation: Avoid including sensitive prompts or media URLs when enabling these options.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/2253128/skills/sanjianke-seedance-video)
- [Video task API](artifact/references/api-create.md)
- [Asset and task API documentation](artifact/SKILL.md)
- [Getting started with a7w](artifact/references/getting-started.md)
- [a7w API platform](https://api.a7w.cn/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown instructions, CLI commands, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Asynchronous video tasks may return task IDs requiring polling; results can include video URLs.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata; bundled SKILL.md lists 1.0.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
