## Description: <br>
RunningHub is a cloud ComfyUI platform for creating AI applications and workflows, including text-to-image, text-to-video, and AI video synthesis across the China and international RunningHub services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YFY-AI](https://clawhub.ai/user/YFY-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to call RunningHub cloud APIs for ComfyUI workflow execution, task status checks, account queries, and workflow management for image and video generation tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: RunningHub API use may send prompts, media, workflow data, or other inputs to a third-party cloud service. <br>
Mitigation: Avoid sending sensitive prompts, private media, secrets, or regulated data unless the user is comfortable sharing them with RunningHub. <br>
Risk: The skill may initiate paid generation or workflow publishing actions through RunningHub. <br>
Mitigation: Confirm paid generation and workflow publishing actions before execution, and use a revocable API key only when needed. <br>
Risk: Authenticated API calls require handling a RunningHub API key. <br>
Mitigation: Use a revocable key, provide it only when needed, and do not expose it in prompts, logs, or shared outputs. <br>


## Reference(s): <br>
- [RunningHub China service](https://www.runninghub.cn) <br>
- [RunningHub international service](https://www.runninghub.ai) <br>
- [RunningHub API documentation](https://www.runninghub.cn/call-api) <br>
- [RunningHub workflow gallery](https://www.runninghub.cn/works-square) <br>
- [ClawHub release page](https://clawhub.ai/YFY-AI/runninghub) <br>
- [Publisher profile](https://clawhub.ai/user/YFY-AI) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, API Calls, Configuration] <br>
**Output Format:** [Markdown with JavaScript examples and API endpoint references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a RunningHub API key for authenticated API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
