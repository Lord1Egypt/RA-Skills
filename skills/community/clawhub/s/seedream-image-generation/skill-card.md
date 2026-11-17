## Description:

Generates and edits images through the Volcengine Seedream API for text-to-image, image-to-image, and general visual creative tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cp7553479](https://clawhub.ai/user/cp7553479)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to generate or transform images with Volcengine Seedream from text prompts or local image inputs, optionally saving generated images to a local directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials and generation payloads may be sent to an arbitrary configured endpoint.

Mitigation: Set SEEDREAM_BASE_URL only to a controlled, trusted HTTPS Volcengine endpoint before use.

Risk: Local image inputs are uploaded for image-to-image generation, and selected image paths or response data may appear in logs or returned output.

Mitigation: Avoid sensitive images, review logs before sharing, and use sandboxed download paths.

Risk: Optional model tools such as web_search can change API behavior.

Mitigation: Enable optional tools only after reviewing their behavior and need for the task.

## Reference(s):

- [Volcengine Seedream image generation API documentation](https://www.volcengine.com/docs/82379/1541523?lang=zh)
- [Volcengine Seedream model list](https://www.volcengine.com/docs/82379/1330310?lang=zh#36969059)
- [ClawHub skill page](https://clawhub.ai/cp7553479/skills/seedream-image-generation)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; script execution returns JSON responses and generated image URLs or local image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SEEDREAM_API_KEY and supports optional SEEDREAM_BASE_URL, image inputs, output format, size, watermark, prompt optimization, model tools, and download directory settings.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
