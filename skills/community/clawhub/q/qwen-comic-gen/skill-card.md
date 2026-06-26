## Description: <br>
Generate or edit images with the packaged Nano Banana Pro, Gemini 3 Pro Image workflow, including text-to-image and image-to-image requests at 1K, 2K, or 4K resolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[icesumer-lgtm](https://clawhub.ai/user/icesumer-lgtm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agent users use this skill to generate new images or edit existing images from natural-language prompts while controlling output resolution and saved filename. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes a large unrelated personal workspace with credentials, memory files, hooks, and agent-behavior instructions. <br>
Mitigation: Review before installing and prefer a repackaged release containing only the skill instructions and image-generation script; rotate any exposed credentials if they are real. <br>
Risk: The workflow sends prompts and optional source images to an external image-generation API and reads an API key from an argument or environment variable. <br>
Mitigation: Use a scoped API key, avoid submitting sensitive prompts or images, and keep credentials out of chat transcripts and committed files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/icesumer-lgtm/qwen-comic-gen) <br>
- [Packaged skill instructions](artifact/SKILL.md) <br>
- [Packaged image generation script](artifact/scripts/generate_image.py) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated PNG file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script saves generated or edited PNG images to the working directory or requested output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
