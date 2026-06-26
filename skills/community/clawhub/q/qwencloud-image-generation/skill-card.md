## Description: <br>
Generates and edits images with QwenCloud Wan and Qwen Image models, including text-to-image, reference-image editing, style transfer, subject consistency, text rendering, and interleaved text-image output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cuixiaoyang123](https://clawhub.ai/user/cuixiaoyang123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and agents use this skill to create image assets, edit reference images, render poster text, and produce mixed text-image content through QwenCloud image-generation APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a QwenCloud API key and may send prompts and selected images to QwenCloud. <br>
Mitigation: Use environment variables or placeholder `.env` entries, never expose plaintext credentials, and confirm that prompt and image content is appropriate to send to QwenCloud. <br>
Risk: Generated images can incur QwenCloud usage charges, especially when multi-image parameters are increased. <br>
Mitigation: Start with one output image during testing and review billing or usage before increasing `n` or `max_images`. <br>
Risk: The skill can prompt agents to install update-related code through an `npx skills add` command. <br>
Mitigation: Treat update prompts as optional and review the repository, command, and any proposed `.agents`, `CLAUDE.md`, or `AGENTS.md` changes before approving installation. <br>


## Reference(s): <br>
- [Execution Guide](references/execution-guide.md) <br>
- [API Guide](references/api-guide.md) <br>
- [Prompt Guide](references/prompt-guide.md) <br>
- [Agent Compatibility](references/agent-compatibility.md) <br>
- [Qwen Image Generation API Sources](references/sources.md) <br>
- [QwenCloud Text-to-Image API Reference](https://docs.qwencloud.com/developer-guides/image-generation/text-to-image) <br>
- [QwenCloud Wan2.6 Image Editing API Reference](https://docs.qwencloud.com/api-reference/image-generation/wan26-image-gen-edit/create-task) <br>
- [QwenCloud Wan2.5 Image Editing API Reference](https://docs.qwencloud.com/api-reference/image-generation/wan25-general-image-editing/create-task) <br>
- [QwenCloud Model List](https://www.qwencloud.com/models) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with JSON API requests, shell commands, and generated image files or image URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local image paths, image URLs, interleaved markdown output, and JSON response summaries.] <br>

## Skill Version(s): <br>
0.2.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
