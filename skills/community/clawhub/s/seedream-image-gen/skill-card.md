## Description:

Seedream 图片生成 helps agents use the Volcengine Ark Seedream image-generation API for text-to-image, image-to-image, multi-image fusion, sequential image generation, and optional web-search-assisted image generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xhuang68](https://clawhub.ai/user/xhuang68)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare Seedream image-generation requests, configure the required Ark API key, and run prompt-based or reference-image workflows that save generated images to a chosen output directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, input image URLs, and reference-image content may be sent to the external Volcengine Ark Seedream service.

Mitigation: Avoid confidential prompts, private images, regulated data, and secrets unless the provider's data handling terms have been reviewed and approved for the use case.

Risk: Passing the Ark API key directly on the command line can expose it through shell history or process listings.

Mitigation: Prefer ARK_API_KEY or a managed secret store instead of the --api-key command option.

## Reference(s):

- [Volcengine Seedream API documentation](https://www.volcengine.com/docs/82379/1541523)
- [ClawHub skill page](https://clawhub.ai/xhuang68/skills/seedream-image-gen)
- [Publisher profile](https://clawhub.ai/user/xhuang68)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference generated image files written by the Seedream helper to the configured output directory.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
