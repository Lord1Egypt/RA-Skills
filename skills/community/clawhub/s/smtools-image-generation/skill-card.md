## Description:

Generate images from text prompts using AI models via OpenRouter, Kie.ai, or YandexART.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bzsega](https://clawhub.ai/user/bzsega)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate or edit images from prompts through provider-backed image generation APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and input images may be sent to external image generation providers.

Mitigation: Avoid confidential prompts or private images unless the selected provider is approved for that data.

Risk: Weak controls around file output paths may allow unintended writes when paths are chosen from untrusted text.

Mitigation: Use a dedicated output directory and do not let untrusted text choose output paths.

Risk: Downloaded image content, especially through the Kie provider, may lack URL and size validation.

Mitigation: Add URL and size validation and lock dependencies before enabling the Kie provider in sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bzsega/skills/smtools-image-generation)
- [OpenRouter](https://openrouter.ai)
- [Kie.ai](https://kie.ai)
- [Yandex Cloud](https://cloud.yandex.ru)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Files]

**Output Format:** [JSON status output plus saved image files and concise user-facing text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires provider API credentials; generated images are written to a local output path.]

## Skill Version(s):

1.9.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
