## Description: <br>
Instantly analyze markdown articles, generate prompts, and seamlessly insert AI illustrations with zero configuration required. Supports Pollinations API (zero-config) with graceful fallback to HuggingFace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wysaid](https://clawhub.ai/user/wysaid) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and documentation maintainers use this skill to add generated illustrations to Markdown articles after reviewing an outline of insertion points and image concepts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Markdown content and generated prompts may be sent to external image-generation services. <br>
Mitigation: Use the skill only with content approved for sharing with Pollinations or Hugging Face, and review the illustration outline before generation. <br>
Risk: Stored or ambient Hugging Face credentials may be used automatically. <br>
Mitigation: Check ~/.config/snap-illustrator/config.json and HF_TOKEN before running, and prefer temporary environment variables for credential use. <br>
Risk: Proxy settings could be persisted into the skill file if artifact guidance is followed directly. <br>
Mitigation: Do not write proxy addresses into SKILL.md; use per-command HTTP_PROXY and HTTPS_PROXY environment variables instead. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wysaid/snap-illustrator) <br>
- [Publisher profile](https://clawhub.ai/user/wysaid) <br>
- [Hugging Face](https://huggingface.co) <br>
- [Hugging Face Stable Diffusion XL inference endpoint](https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0) <br>
- [Pollinations image generation endpoint](https://image.pollinations.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown edits with image links, generated image files, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js for image generation; may use HF_TOKEN when Hugging Face fallback is needed.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
