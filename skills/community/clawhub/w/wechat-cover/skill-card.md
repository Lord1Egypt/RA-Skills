## Description: <br>
Generate WeChat official account cover images with proper 2.35:1 aspect ratio. Supports OpenAI DALL-E and Gemini image generation with customizable styles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[derekdong-star](https://clawhub.ai/user/derekdong-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content teams, and WeChat official account publishers use this skill to generate article cover images from a title, topic, provider, style, and resolution settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Article titles, topics, and generated prompts may be sent to the configured image provider. <br>
Mitigation: Avoid confidential unpublished content in prompts and use providers approved for the intended content. <br>
Risk: A custom OpenAI-compatible proxy can receive prompts and API traffic. <br>
Mitigation: Prefer official OpenAI or Gemini endpoints unless the proxy is trusted and approved. <br>
Risk: API keys are required for image generation. <br>
Mitigation: Keep API keys in private environment variables or local configuration and do not commit real credentials. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/derekdong-star/wechat-cover) <br>
- [OpenAI Platform API keys](https://platform.openai.com/api-keys) <br>
- [Google AI Studio API keys](https://aistudio.google.com/app/apikey) <br>


## Skill Output: <br>
**Output Type(s):** [files, shell commands, configuration, guidance] <br>
**Output Format:** [PNG image files with Markdown usage guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated images are cropped and resized to 900x383 PNG, with date-and-title filenames when no filename is supplied.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
