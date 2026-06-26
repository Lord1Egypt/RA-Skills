## Description: <br>
Uses Alibaba Cloud DashScope Wan2.6-t2i to generate images from text prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baokui](https://clawhub.ai/user/baokui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to generate images from text through Alibaba Cloud DashScope, with optional negative prompts and image size choices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts are sent to Alibaba Cloud DashScope, which can expose secrets, private data, or confidential creative direction if users include them. <br>
Mitigation: Avoid private or confidential prompt content and use a revocable API key where possible. <br>
Risk: Unusual quotes or JSON-like prompt text may produce malformed or unexpected API requests. <br>
Mitigation: Review and simplify prompts with special quoting or JSON-like content before running the shell script. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baokui/wan-text2image) <br>
- [DashScope multimodal generation endpoint](https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Guidance] <br>
**Output Format:** [JSON API response, typically containing generated image data or image URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DASHSCOPE_API_KEY and curl; supports prompt, negative prompt, and image size inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
