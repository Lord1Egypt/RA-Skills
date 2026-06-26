## Description: <br>
Generate persona-consistent selfie images and send to any OpenClaw channel. Supports Gemini, fal, and laozhang.ai providers, multi-reference avatar blending. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tower1229](https://clawhub.ai/user/tower1229) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and agent operators use Stella Selfie to generate persona-consistent selfie or third-person photo images from a configured identity, then send the generated media to a selected OpenClaw-connected channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Provider API keys may incur usage cost when the skill generates images. <br>
Mitigation: Use provider keys with spending limits where possible and install the skill only when image generation through the configured providers is intended. <br>
Risk: Configured avatar images and prompt text are sent to the selected image provider as part of normal generation. <br>
Mitigation: Keep avatar directories and public avatar URLs limited to intended reference photos, and choose the provider configuration deliberately before use. <br>
Risk: Generated images can be sent to shared OpenClaw-connected channels. <br>
Mitigation: Verify the target channel and recipient before sending images, especially in shared spaces. <br>


## Reference(s): <br>
- [Timeline Integration](references/timeline-integration.md) <br>
- [Stella homepage](https://github.com/tower1229/Stella) <br>
- [ClawHub skill page](https://clawhub.ai/tower1229/stella-selfie) <br>


## Skill Output: <br>
**Output Type(s):** [Image media, Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Generated images sent through OpenClaw, with concise text confirmations or actionable failure messages and Markdown setup guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provider-specific API calls may use local avatar files, public avatar URLs, prompt text, target channel details, and caption text; Gemini and laozhang.ai generated files are written locally and deleted after successful send.] <br>

## Skill Version(s): <br>
1.3.3 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
