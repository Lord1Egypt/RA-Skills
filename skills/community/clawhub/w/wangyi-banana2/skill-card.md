## Description:

Generate images and videos through the WangYi Banana API, including text-to-image, image-to-image, text-to-video, image-to-video, and character creation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zxq790909-maker](https://clawhub.ai/user/zxq790909-maker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to generate or edit images, generate short videos, and create reusable video characters through WangYi Banana models. It is aimed at media-production workflows where an agent guides model selection, parameter choices, file delivery, and cost reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed if users paste credentials directly into chat.

Mitigation: Use WANGYI_API_KEY or local OpenClaw configuration, and rotate any key already shared conversationally.

Risk: Prompts, personal media, and generated outputs are handled by the WangYi Banana service.

Mitigation: Avoid confidential prompts or personal media unless the service is trusted, and keep outputs in the default temporary directory unless another path is intentional.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zxq790909-maker/skills/wangyi-banana2)
- [WangYi Banana API homepage](https://ai.t8star.cn)
- [API key setup guide](artifact/references/api-key-setup.md)
- [Image generation guide](artifact/references/image-generation.md)
- [Video generation guide](artifact/references/video-generation.md)
- [Output delivery guide](artifact/references/output-delivery.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated media or JSON file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated image and video files are delivered from the configured output directory; character creation can produce JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
