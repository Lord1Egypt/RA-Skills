## Description: <br>
内容引擎 helps agents deconstruct Xiaohongshu reference posts and generate brand-aware scripts, captions, cover copy, tags, image assets, and optional video outputs using a maintained content graph. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dizhu](https://clawhub.ai/user/dizhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content teams, creators, and agent operators use this skill to turn Xiaohongshu reference links into structured deconstruction cards, then generate brand-aligned content packages from those cards and the local brand graph. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires TikHub, Ofox/OpenRouter, and Ark credentials and sends XHS content, brand graph context, product details, and prompts to those providers. <br>
Mitigation: Install only when those providers are approved for the intended content, keep .env files private, and avoid confidential campaign material unless provider sharing is acceptable. <br>
Risk: Custom provider base URLs can route credentials or content to untrusted hosts. <br>
Mitigation: Do not set OFOX_BASE_URL, ARK_BASE_URL, or TIKHUB_BASE_URL to untrusted hosts. <br>
Risk: Real Seedance video generation can use paid provider capacity. <br>
Mitigation: Use --no-real-video until paid video generation is intended. <br>
Risk: Generated workspaces may contain confidential campaign material. <br>
Mitigation: Review generated workspaces before sharing and delete them when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dizhu/qianxun-content-engine) <br>
- [Output template](references/output-template.md) <br>
- [Example image workflow](references/example-image.md) <br>
- [Example video workflow](references/example-video.md) <br>
- [TikHub](https://tikhub.io) <br>
- [Ofox](https://ofox.ai) <br>
- [OpenRouter](https://openrouter.ai) <br>
- [Volcengine Ark API key console](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, generated media workspace files, JSON data, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local content workspaces containing deconstruction cards, comments, frames, images, scripts, captions, cover text, tags, prompts, and generated media.] <br>

## Skill Version(s): <br>
0.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
