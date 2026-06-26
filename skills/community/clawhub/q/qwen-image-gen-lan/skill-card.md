## Description: <br>
阿里云千问文生图模型（Qwen-Image）技能，支持图像生成。当用户要求AI生成图片、画图、文生图、text-to-image，或提到千问、阿里云生图时使用。支持中英文提示词，可指定画面尺寸、风格参数等。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanlan314](https://clawhub.ai/user/lanlan314) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent prepare DashScope/Qwen image-generation requests from Chinese or English prompts, choose supported Qwen-Image models and aspect ratios, and return generated image URLs. <br>

### Deployment Geography for Use: <br>
Global, with DashScope regional endpoint and API-key availability determining where requests are sent. <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and generation parameters are sent to Alibaba DashScope/Qwen. <br>
Mitigation: Avoid confidential or sensitive prompts unless the user is comfortable sending them to DashScope. <br>
Risk: DashScope API key use can affect quota or billing. <br>
Mitigation: Keep DASHSCOPE_API_KEY out of shared output and monitor key usage. <br>
Risk: Generated image URLs are temporary according to the artifact documentation. <br>
Mitigation: Save needed outputs promptly instead of relying on the returned URL remaining available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lanlan314/qwen-image-gen-lan) <br>
- [千问文生图 API 详细参考](references/api.md) <br>
- [DashScope API key documentation](https://help.aliyun.com/zh/model-studio/get-api-key) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash and JSON examples; generated image URLs in API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DASHSCOPE_API_KEY; generated image URLs are documented as valid for 24 hours.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
