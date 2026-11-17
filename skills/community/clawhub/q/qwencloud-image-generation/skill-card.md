## Description:

Generates and edits images with QwenCloud Wan and Qwen Image models for text-to-image, reference-image editing, style transfer, subject consistency, text rendering, multi-image composition, and interleaved text-image output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cuixiaoyang123](https://clawhub.ai/user/cuixiaoyang123)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to generate and edit images through QwenCloud models from natural-language prompts and optional reference images. It supports creative asset generation, posters, style transfer, subject-consistent edits, multi-image composition, and interleaved text-image content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: QwenCloud receives prompts, reference images, and API-authenticated requests during normal image generation and editing.

Mitigation: Avoid sensitive prompts or images, provide only the needed QwenCloud API key through environment variables, and do not expose credential values in logs or responses.

Risk: The skill includes an update-check and install prompt workflow with persistent agent-state behavior.

Mitigation: Review any ACTION_REQUIRED or UPDATE_AVAILABLE signal before acting, and decline or disable the update-check prompt unless the mutable install path is trusted.

Risk: The suggested update installation path uses npx to install external skill code.

Mitigation: Inspect and approve the source and requested update before running the installation command; prefer reviewed or pinned releases where available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cuixiaoyang123/skills/qwencloud-image-generation)
- [Qwen Image Generation API Sources](references/sources.md)
- [Qwen Image Generation API Supplementary Guide](references/api-guide.md)
- [Qwen Image Generation Execution Guide](references/execution-guide.md)
- [Image Generation Prompt Guide](references/prompt-guide.md)
- [QwenCloud text-to-image API reference](https://docs.qwencloud.com/developer-guides/image-generation/text-to-image)
- [Wan2.6 Image API reference](https://docs.qwencloud.com/api-reference/image-generation/wan26-image-gen-edit/create-task)
- [QwenCloud model list](https://www.qwencloud.com/models)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Image files, JSON responses, Markdown for interleaved output, and shell or Python command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local_path, local_paths, image_url, image_urls, image_count, width, height, seed, and interleaved_content.]

## Skill Version(s):

0.2.1 (source: server release evidence, created 2026-04-30)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
