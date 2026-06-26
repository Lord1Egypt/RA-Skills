## Description: <br>
Unified multi-platform AI image generation for Volcengine Seedream, Alibaba Qwen Image, and Google Gemini (Nano Banana), with model switching through a dropdown selector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sangjiexun](https://clawhub.ai/user/sangjiexun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to add multi-provider AI image generation to the paint page, select a model, configure provider API keys, and submit prompts through the configured provider. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reviewed package is incomplete and references missing proxy and injection scripts that would handle API keys, prompts, and provider routing. <br>
Mitigation: Review the missing proxy and injection scripts from a trusted source before installing or running the skill. <br>
Risk: Prompts, images, and configured API keys may be transmitted to the selected third-party image provider through the local proxy flow. <br>
Mitigation: Configure only intended providers, restrict and protect API keys, and avoid submitting sensitive prompts or images unless that provider transmission is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sangjiexun/uni-image) <br>


## Skill Output: <br>
**Output Type(s):** [Configuration, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown with configuration steps and curl command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses provider API keys for Volcengine Ark, Alibaba DashScope, and Google Gemini; provider responses may include generated image data or image URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
