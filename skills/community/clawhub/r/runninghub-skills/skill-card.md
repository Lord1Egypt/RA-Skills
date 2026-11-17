## Description:

Generates images, videos, audio, and 3D models through 170+ RunningHub API endpoints, and runs RunningHub AI Applications/custom ComfyUI workflows by webappId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hm-runninghub](https://clawhub.ai/user/hm-runninghub)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and creative teams use this skill to generate or transform images, videos, audio, and 3D assets through RunningHub endpoints, and to run custom RunningHub AI Application workflows from an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles paid RunningHub API keys and may receive keys through chat or local configuration.

Mitigation: Use a protected secret store or tightly scoped environment variable, do not paste API keys into chat, rotate any key previously shared, and monitor billing.

Risk: Generated-media workflows can upload user media to an external RunningHub service for processing.

Mitigation: Avoid uploading sensitive media unless the user consents to external processing.

Risk: Voice cloning can create misuse risk when the source voice owner has not consented.

Mitigation: Use voice cloning only with clear permission from the voice owner.

Risk: The release security verdict is suspicious and recommends review before installation.

Mitigation: Review and scan the skill before deployment.

## Reference(s):

- [RunningHub Skill Page](https://clawhub.ai/hm-runninghub/skills/runninghub-skills)
- [RunningHub Homepage](https://www.runninghub.cn)
- [RunningHub OpenAPI v2](https://www.runninghub.cn/openapi/v2)
- [AI Application](references/ai-application.md)
- [API Key Setup](references/api-key-setup.md)
- [Image Model Selection](references/image-models.md)
- [Output and Delivery](references/output-delivery.md)
- [Video Model Selection](references/video-models.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands, JSON/text status, and generated media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce image, video, audio, 3D, or text outputs through paid RunningHub API calls.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
