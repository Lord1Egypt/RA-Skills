## Description: <br>
Generate images from text prompts using AI models via OpenRouter, Kie.ai, or YandexART. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bzSega](https://clawhub.ai/user/bzSega) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to generate or edit images from natural-language prompts through configured third-party image providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and input images are sent to the selected external image provider. <br>
Mitigation: Avoid sensitive prompts or private images, and choose providers according to the user's privacy and compliance requirements. <br>
Risk: Provider API keys can incur usage charges or expose account access if mishandled. <br>
Mitigation: Use revocable keys with spending limits, keep keys out of logs and shared output, and rotate them if exposure is suspected. <br>
Risk: Custom output paths can write generated files outside the default skill output directory. <br>
Mitigation: Prefer the default output directory or review explicit output paths before running generation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bzSega/smtools-image-generation) <br>
- [OpenRouter](https://openrouter.ai) <br>
- [Kie.ai](https://kie.ai) <br>
- [Yandex Cloud](https://cloud.yandex.ru) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, code, guidance] <br>
**Output Format:** [JSON status output with generated image files saved to disk, plus agent-facing guidance and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and provider API credentials; default output is an image file path returned in JSON.] <br>

## Skill Version(s): <br>
1.9.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
