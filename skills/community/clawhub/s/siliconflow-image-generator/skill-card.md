## Description: <br>
SiliconFlow text-to-image and image-to-image generation for covers, posters, and campaign creatives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangziiiiii](https://clawhub.ai/user/wangziiiiii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to generate social covers, posters, campaign creatives, and image variations from prompts or reference images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential scoping could expose a broader API key than intended. <br>
Mitigation: Prefer a dedicated SILICONFLOW_API_KEY and avoid relying on generic API_KEY or memory-search configuration. <br>
Risk: Prompts or private reference images are sent to SiliconFlow for processing. <br>
Mitigation: Do not submit sensitive prompts or private images unless the user is comfortable sharing them with SiliconFlow. <br>
Risk: Server security evidence marks the release as suspicious. <br>
Mitigation: Review the skill before installing and confirm the credential and data-disclosure behavior is acceptable. <br>


## Reference(s): <br>
- [SiliconFlow Console](https://siliconflow.cn) <br>
- [SiliconFlow Image Generation API Endpoint](https://api.siliconflow.cn/v1/images/generations) <br>
- [ClawHub Skill Page](https://clawhub.ai/wangziiiiii/siliconflow-image-generator) <br>
- [Publisher Profile](https://clawhub.ai/user/wangziiiiii) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API Calls, Shell commands, Configuration] <br>
**Output Format:** [JSON response containing SiliconFlow image-generation results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a SiliconFlow API key and sends prompts and optional reference images to SiliconFlow for processing.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
