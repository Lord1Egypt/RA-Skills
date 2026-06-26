## Description: <br>
Directly connects agents to Alibaba Cloud DashScope Qwen Wan 2.6 video generation for text-to-video and image-to-video workflows without an intermediate proxy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuchhao](https://clawhub.ai/user/wuchhao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to generate short videos from text prompts or reference image URLs through Alibaba Cloud DashScope, with controls such as duration and resolution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, referenced image URLs, and DashScope credentials are used with Alibaba Cloud DashScope. <br>
Mitigation: Avoid confidential prompts, private image URLs, or regulated data unless account terms and organization policy allow it; configure DASHSCOPE_API_KEY through the environment. <br>
Risk: Video generation and polling may incur provider charges. <br>
Mitigation: Monitor DashScope usage, quotas, and account billing before running generation jobs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wuchhao/qwen-wan-video) <br>
- [DashScope API endpoint](https://dashscope.aliyuncs.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown with Python and bash code blocks; generated video URLs returned as strings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses DASHSCOPE_API_KEY and asynchronous polling; generated video duration is up to 5 seconds per artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
