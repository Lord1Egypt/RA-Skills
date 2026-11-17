## Description:

Generate and edit images with Qwen Image via the DashScope API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huiya-code](https://clawhub.ai/user/huiya-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate images from prompts and edit or fuse one to three input images through Qwen Image via DashScope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, selected input images, and the API key can be sent to the configured DashScope endpoint.

Mitigation: Use only trusted endpoints, avoid sensitive prompts or images, and set DASHSCOPE_ENDPOINT only when you control and trust that server.

Risk: The skill downloads unvalidated response URLs and saves generated media locally.

Mitigation: Run the skill in a controlled directory, avoid untrusted project folders with .env files, and review generated outputs before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huiya-code/skills/qwen-skill)
- [Publisher profile](https://clawhub.ai/user/huiya-code)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [One-line MEDIA reference with generated image files and optional JSON result data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and DASHSCOPE_API_KEY; supports text-to-image and one-to-three-image editing workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
