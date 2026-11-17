## Description:

A Chinese-language image-generation tool that uses the DashScope API to create comics, illustrations, posters, and other images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bjbook](https://clawhub.ai/user/bjbook)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can generate images from Chinese or other text prompts, select image models and dimensions, and optionally provide reference images where supported.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts are written to a local interaction log, which may retain sensitive input.

Mitigation: Disable or control prompt logging, protect or remove existing log files, and avoid submitting sensitive prompts.

Risk: The downloader follows arbitrary HTTP or HTTPS image addresses returned by the API.

Mitigation: Review and constrain permitted download hosts or verify each returned address before allowing the download.

Risk: Prompts, selected reference images, and the API key are sent to the configured endpoint.

Mitigation: Use only a trusted endpoint, understand its data handling, and avoid sensitive prompts or reference images.

Risk: The tool can fall back to reading an API key from local files.

Mitigation: Review the fallback paths, restrict access to key files, and prefer a controlled credential source.

## Reference(s):

- [Skill homepage](http://openclaw.bjbook.net/)
- [ClawHub skill release](https://clawhub.ai/bjbook/skills/zhz-image-gen)
- [Publisher profile](https://clawhub.ai/user/bjbook)
- [DashScope image generation API endpoint](https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation)

## Skill Output:

**Output Type(s):** [Images]

**Output Format:** [Image file saved to the requested path; the response format is determined by the image-generation API.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-driven generation with selectable model, quality, aspect ratio, and dimensions; optional reference images are supported by compatible models.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
