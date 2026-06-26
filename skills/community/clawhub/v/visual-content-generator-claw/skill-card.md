## Description: <br>
AI-driven visual content generation skill for creating posters, social media images, video covers, and virtual-human backgrounds from natural-language or structured requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tujinsama](https://clawhub.ai/user/tujinsama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and agent users use this skill to turn visual requirements into image-generation prompts and produce local image files for posters, social posts, covers, and backgrounds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud image generation can expose prompts to an external model provider when DALL-E 3 is selected. <br>
Mitigation: Use non-sensitive prompts for cloud generation and prefer local Stable Diffusion when prompt privacy is required. <br>
Risk: The generation script may use sensitive API credentials such as OPENAI_API_KEY. <br>
Mitigation: Restrict API key permissions, avoid embedding keys in prompts or files, and keep credentials in environment variables. <br>
Risk: Optional Feishu uploads can share generated output beyond the local workspace. <br>
Mitigation: Approve uploads only for outputs intended to be shared and review generated images before upload. <br>
Risk: Generated text inside images may be distorted or unreliable. <br>
Mitigation: Review image text manually and use separate design tooling for precise final typography when needed. <br>


## Reference(s): <br>
- [视觉风格规范](references/visual-style-guide.md) <br>
- [Prompt 模板库](references/prompt-templates.md) <br>
- [平台尺寸规范](references/platform-size-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/tujinsama/visual-content-generator-claw) <br>
- [Publisher profile](https://clawhub.ai/user/tujinsama) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and generated local image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save generated PNG files locally and can emit a JSON result with file paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
