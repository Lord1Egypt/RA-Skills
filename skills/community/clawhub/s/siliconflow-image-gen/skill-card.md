## Description:

Generate images using SiliconFlow API (FLUX.1, Stable Diffusion, etc.).

This skill is ready for commercial/non-commercial use.

## Publisher:

[lilei0311](https://clawhub.ai/user/lilei0311)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to generate images from text prompts through the SiliconFlow API, optionally selecting supported FLUX.1 or Stable Diffusion models and saving generated images locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A paid or high-privilege SiliconFlow API key could be exposed locally through the skill's broad command execution and curl-based credential handling.

Mitigation: Use a limited SiliconFlow API key with spending controls, review the skill before installation, and consider replacing the curl subprocess with an in-process HTTPS client or narrower runtime permission.

Risk: Private prompt content may be sent to SiliconFlow during image generation.

Mitigation: Avoid prompts containing private, regulated, or confidential data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lilei0311/skills/siliconflow-image-gen)
- [SiliconFlow API endpoint](https://api.siliconflow.cn/v1)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, files]

**Output Format:** [JSON status output with an image URL and optional downloaded image file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SILICONFLOW_API_KEY or an OpenClaw config entry; prompts and selected model parameters are sent to SiliconFlow.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
