## Description: <br>
Generate videos using Alibaba Cloud DashScope Wan text-to-video APIs, including async task submission, status polling, and local MP4 download. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[547895019](https://clawhub.ai/user/547895019) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to create short videos from text prompts through Alibaba Cloud DashScope Wan models, then retrieve the generated MP4 for local use. It supports common agent workflows for submitting generation jobs, polling completion, and downloading media. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill disables HTTPS certificate verification while sending an API key. <br>
Mitigation: Review and patch the scripts before use, remove curl -k, and use a limited DashScope API key where possible. <br>
Risk: Prompt, audio URL, and generated media handling may expose sensitive inputs or overwrite an existing MP4 path. <br>
Mitigation: Avoid sensitive prompts or audio URLs and choose an output path where overwriting a file would not matter. <br>


## Reference(s): <br>
- [DashScope Wan t2v API notes](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/547895019/qwen-video) <br>
- [DashScope video synthesis endpoint](https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated task or media paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce DashScope task IDs, signed video URLs, and local MP4 file paths.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
