## Description:

Helps agents submit AI clothing try-on jobs from model and garment images and retrieve the resulting images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2253128](https://clawhub.ai/user/2253128)

### License/Terms of Use:

MIT

## Use Case:

Creators and developers use this skill to generate virtual outfit previews from model and clothing images and check the results of submitted jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled client can use an a7w API key to access marketplace services beyond the advertised try-on workflow.

Mitigation: Use a limited, revocable key where available and review commands before running them.

Risk: Submitted images may contain sensitive personal content, and API calls may spend account points.

Mitigation: Obtain consent before sharing personal images and check usage and pricing before submitting jobs.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/2253128/skills/sanjianke-dressing-diffusion)
- [Getting started and API key setup](references/getting-started.md)
- [Submit try-on task API](references/api-submit.md)
- [Query try-on result API](references/api-query.md)
- [a7w API marketplace](https://api.a7w.cn/)

## Skill Output:

**Output Type(s):** [JSON, Guidance, Shell commands]

**Output Format:** [JSON API responses and Markdown instructions with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Submissions return a task ID; completed tasks return image URLs.]

## Skill Version(s):

1.0.7 (source: ClawHub release metadata; bundled SKILL.md says 1.0.6)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
