## Description:

Generate images via BigModel APIs and send them as chat images (e.g. Feishu). Invoke when user asks to create a single picture with specific style/size.

This skill is ready for commercial/non-commercial use.

## Publisher:

[henrybao91](https://clawhub.ai/user/henrybao91)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate a single image from a user prompt with selectable BigModel image models, image sizes, watermark settings, and a local output path. It can also support Feishu workflows by returning a generated local image file for sending as a chat image.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read local TOOLS.md files to locate credentials when ZHIPU_API_KEY is not set in the environment.

Mitigation: Install only after review and provide ZHIPU_API_KEY explicitly through the declared environment variable; prefer a version that removes ambient credential lookup.

Risk: The script downloads remote image content and saves it to disk with weak URL and file-size safeguards.

Mitigation: Run in a constrained workspace, use non-sensitive prompts, and prefer a version that restricts downloaded image URLs and file sizes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/henrybao91/skills/zhipu-image-generator)
- [BigModel image generation API endpoint](https://open.bigmodel.cn/api/paas/v4/images/generations)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and a generated local image file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZHIPU_API_KEY and writes the downloaded generated image to disk.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
