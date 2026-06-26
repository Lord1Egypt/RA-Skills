## Description: <br>
Analyze images and videos using Qwen Vision API (Alibaba Cloud DashScope). Supports image understanding, OCR, visual reasoning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[perchouli](https://clawhub.ai/user/perchouli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to send user-selected images to Alibaba Cloud DashScope Qwen Vision models for image description, OCR, chart interpretation, and visual question answering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images and prompts are sent to Alibaba Cloud DashScope for analysis. <br>
Mitigation: Use the skill only with images and prompts you are authorized to share with that provider. <br>
Risk: DashScope API keys may allow billable API usage if exposed. <br>
Mitigation: Store API keys in approved configuration or environment variables and avoid sharing them in prompts, logs, or command history. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/perchouli/qwen-vision) <br>
- [Alibaba Cloud DashScope](https://dashscope.aliyuncs.com/) <br>
- [DashScope API key console](https://dashscope.console.aliyun.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text responses from the vision API, with Markdown usage examples in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a DashScope API key; image and prompt content are sent to Alibaba Cloud DashScope.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
