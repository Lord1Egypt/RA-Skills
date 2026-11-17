## Description:

Generate images with Seedream 5 through the BytePlus Ark API using a direct API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gamaleldientarek](https://clawhub.ai/user/gamaleldientarek)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers with a Seedream or BytePlus Ark API key use this skill to generate images from prompts through the BytePlus Ark API and save the resulting image locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and generation requests are sent to BytePlus Ark.

Mitigation: Avoid sensitive prompt text and install only when external API use with a local Seedream API key is acceptable.

Risk: Credential handling uses SEEDREAM_API_KEY and may source a local environment file.

Mitigation: Prefer passing SEEDREAM_API_KEY through the environment and review local credential storage before use.

Risk: The output filename can be caller-controlled.

Mitigation: Use trusted output paths and do not allow untrusted input to choose the output filename.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gamaleldientarek/skills/seedream-5-byteplus)
- [BytePlus Ark image generation endpoint](https://ark.ap-southeast.bytepluses.com/api/v3/images/generations)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands; script output is a saved image file path.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses SEEDREAM_API_KEY and optional SEEDREAM_MODEL and SEEDREAM_SIZE environment variables; the output file path may be caller-specified or generated with a timestamped default.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
