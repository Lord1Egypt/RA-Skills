## Description: <br>
使用字节跳动豆包 Doubao SeeDream 模型生成高质量图片，支持文生图、AI 绘图和插画创作。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yy756127197](https://clawhub.ai/user/yy756127197) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to generate images from Chinese or English text prompts through Volcengine ARK's Doubao SeeDream 5.0 model and save the resulting image locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts are sent to the third-party Volcengine ARK API and may expose sensitive user input. <br>
Mitigation: Avoid secrets, private business text, and sensitive personal data in prompts; review prompts before running the skill. <br>
Risk: Diagnostic guidance can partially print the ARK API key. <br>
Mitigation: Remove or avoid key-printing diagnostics and keep API keys in environment variables or a managed secret store. <br>
Risk: The release was flagged for unsafe advice about bypassing content filters. <br>
Mitigation: Review and remove content-filter bypass guidance before relying on the skill, and follow the provider's content policy. <br>
Risk: The skill uses a paid API key and can incur external service costs. <br>
Mitigation: Set usage limits, monitor billing, and restrict the API key to the minimum permissions needed for image generation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yy756127197/yy756127197-doubao-image) <br>
- [Publisher profile](https://clawhub.ai/user/yy756127197) <br>
- [Volcengine ARK documentation](https://www.volcengine.com/docs/82379) <br>
- [Doubao product information](https://www.volcengine.com/product/doubao) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with shell and Python commands; generated images are saved as local PNG files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ARK_API_KEY, sends prompts to Volcengine ARK, and writes images to a configurable output directory.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata, SKILL.md metadata, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
