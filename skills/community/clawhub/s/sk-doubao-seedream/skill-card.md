## Description:

Helps an agent use Volcengine Ark Doubao Seedream models to generate images from text prompts and edit existing images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trylovecatch](https://clawhub.ai/user/trylovecatch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to configure a Volcengine API key, choose a supported Doubao Seedream model, and run text-to-image or image-to-image generation from command-line or interactive workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Volcengine API keys and can store a key in config.json.

Mitigation: Prefer VOLCENGINE_API_KEY or session-only entry, avoid saving keys in config.json, and avoid using the config display option when a stored key is present.

Risk: Prompts and input images are submitted to Volcengine Ark for third-party processing.

Mitigation: Do not submit sensitive prompts or private images unless Volcengine processing is acceptable for the user and use case.

Risk: Security evidence marks the release as suspicious because API-key handling should be reviewed before installation.

Mitigation: Review the skill before installing with a real Volcengine API key and follow the provided security guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/trylovecatch/skills/sk-doubao-seedream)
- [Publisher profile](https://clawhub.ai/user/trylovecatch)
- [Volcengine Ark image generation API documentation](https://www.volcengine.com/docs/82379/1541523)
- [Volcengine Ark console](https://console.volcengine.com/ark)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python CLI usage, and generated image files from the external API.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are written to user-selected local paths; prompts, optional source images, and API keys are sent to Volcengine Ark when generation commands run.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
