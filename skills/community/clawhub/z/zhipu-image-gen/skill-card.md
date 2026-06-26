## Description: <br>
AI text-to-image generation using Zhipu AI's GLM-Image model for Chinese or English prompts, including configurable image sizes and optional watermarking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codeteenager](https://clawhub.ai/user/codeteenager) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate PNG images from text prompts through Zhipu AI's GLM-Image service. It is useful when an agent needs to turn a user-provided visual description into an image file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts are sent to Zhipu AI's external image generation service and may consume the user's API quota. <br>
Mitigation: Use only prompts appropriate for Zhipu AI processing, avoid confidential or personal data, and monitor account quota and billing. <br>
Risk: The skill requires a ZHIPU_API_KEY for API access. <br>
Mitigation: Keep the API key private, provide it through the environment or the skill's local .env file, and avoid sharing logs or files that expose credentials. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/codeteenager/zhipu-image-gen) <br>
- [Zhipu AI Open Platform](https://open.bigmodel.cn/) <br>
- [Zhipu Image Generation API Endpoint](https://open.bigmodel.cn/api/paas/v4/images/generations) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration instructions] <br>
**Output Format:** [PNG image files saved to disk with concise terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZHIPU_API_KEY, curl, and jq; defaults to the glm-image model and 1280x1280 output size.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
