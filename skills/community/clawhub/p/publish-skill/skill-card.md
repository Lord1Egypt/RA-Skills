## Description: <br>
通用文生图技能。使用 MiniMax、OpenAI、DALL-E、Stability 等模型生成图片。用户需要配置自己的 API Key（MINIMAX_API_KEY、OPENAI_API_KEY 等）。当用户需要生成图片、AI绘图时使用此技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoliang1319-cloud](https://clawhub.ai/user/xiaoliang1319-cloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to configure their own image-provider API key and generate images from text prompts through MiniMax, OpenAI DALL-E, or Stability AI. It is intended for users who need agent-assisted AI image generation with provider selection based on available credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts may be sent to a configured third-party image provider. <br>
Mitigation: Avoid entering secrets or sensitive personal or business data in prompts. <br>
Risk: Using provider APIs may consume the user's paid quota. <br>
Mitigation: Configure only the intended provider key and prefer revocable or limited keys where available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaoliang1319-cloud/publish-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, API calls, Images] <br>
**Output Format:** [Markdown guidance with shell environment-variable examples and generated image outputs from the configured provider] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the user's configured provider API key and provider quota.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
