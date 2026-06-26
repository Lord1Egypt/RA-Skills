## Description: <br>
Uses Tongyi Wanxiang 2.6 to generate videos from text prompts or image inputs through a Node.js script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangshengli0421](https://clawhub.ai/user/wangshengli0421) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create short videos with Alibaba DashScope from text prompts or from an image URL plus a prompt. It is suited for workflows that need a generated video URL as the downstream artifact. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and image URLs are sent to Alibaba DashScope for video generation. <br>
Mitigation: Avoid confidential prompts or private image URLs unless the deployment has approved that data sharing. <br>
Risk: The skill requires a DashScope API key and may consume quota or incur costs. <br>
Mitigation: Use a dedicated key, monitor usage, and rotate or revoke the key if it is no longer needed. <br>


## Reference(s): <br>
- [Tianshu Wan Video on ClawHub](https://clawhub.ai/wangshengli0421/tianshu-wan-video) <br>
- [Alibaba DashScope API endpoint used by the skill](https://dashscope.aliyuncs.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, text] <br>
**Output Format:** [Console text containing a VIDEO_URL value] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DASHSCOPE_API_KEY and sends prompts or image URLs to Alibaba DashScope.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
