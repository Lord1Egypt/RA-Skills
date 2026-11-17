## Description:

Generate images with the WuyinKeji GPT-Image-2 API, including text-to-image prompts, reference image URLs, aspect ratio hints, and asynchronous result polling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alex-shen1121](https://clawhub.ai/user/alex-shen1121)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create images through WuyinKeji GPT-Image-2 from prompts, optionally with reference image URLs, and retrieve completed image files after asynchronous polling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials are sent to the provider and may appear in polling URLs.

Mitigation: Use a rotated, limited WuyinKeji API key and avoid exposing command history, logs, or URLs that contain the key.

Risk: Prompts and reference image URLs are submitted to a third-party image generation provider.

Mitigation: Avoid sensitive prompts, private images, regulated data, or confidential URLs unless this provider and use case have been approved.

Risk: Generated result URLs are downloaded by the helper script.

Mitigation: Validate result URLs and scan downloaded files before using them in production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alex-shen1121/skills/wuyin-gpt-image2)
- [WuyinKeji async image generation endpoint](https://api.wuyinkeji.com/api/async/image_gpt)
- [WuyinKeji async task detail endpoint](https://api.wuyinkeji.com/api/async/detail)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-supplied WuyinKeji API key; helper usage may download generated image files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
