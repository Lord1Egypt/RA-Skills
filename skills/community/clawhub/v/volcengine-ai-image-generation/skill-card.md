## Description:

Image generation workflow on Volcengine AI services. Use when users need text-to-image, style variants, prompt refinement, or deterministic image generation parameters and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to generate and iterate images through Volcengine AI services with structured prompts, generation parameters, and troubleshooting guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image prompts and generation settings may be sent to Volcengine/ARK services.

Mitigation: Confirm users are comfortable with that data sharing before installation and avoid submitting sensitive prompt content.

Risk: API credentials could be exposed if embedded in skill files or prompts.

Mitigation: Configure required credentials through the user's normal trusted environment rather than embedding them in the skill.

## Reference(s):

- [Sources](references/sources.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, configuration, guidance]

**Output Format:** [Markdown with image links or files, prompts, parameter settings, and troubleshooting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated image links or files together with the prompt and generation parameters used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
