## Description:

videogenCN helps agents generate short video clips from text prompts, source images, first/last frames, or reference images using Chinese video models from Bailian, Jimeng, MiniMax, and Hunyuan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agents365-ai](https://clawhub.ai/user/agents365-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content teams use this skill to refine Chinese video prompts, choose provider and model parameters, submit asynchronous video generation jobs, and retrieve MP4 outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected images are sent to the named video providers.

Mitigation: Use the skill only with content approved for those providers, and avoid submitting sensitive images or secrets in prompts.

Risk: A provider setting can redirect DashScope API keys and submitted media to an arbitrary endpoint.

Mitigation: Keep DASHSCOPE_API_BASE limited to the documented cn, sg, or us endpoints before running generation.

Risk: Downloaded result files are not tightly validated.

Mitigation: Review generated MP4 files in a controlled environment before sharing or reusing them.

Risk: Install risk is higher without isolated and pinned Python dependencies.

Mitigation: Use a virtual environment and pin dependencies before installing or running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agents365-ai/skills/videogencn)
- [Volcengine Ark console](https://console.volcengine.com/ark/)
- [MiniMax platform](https://platform.minimax.io)
- [Tencent Hunyuan console](https://console.cloud.tencent.com/hunyuan)
- [Alibaba Cloud Bailian console](https://bailian.console.aliyun.com/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files]

**Output Format:** [Markdown guidance with inline shell commands, JSON status envelopes, and downloaded MP4 files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Asynchronous video jobs require provider API keys; result URLs expire after 24 hours, so the skill downloads MP4 outputs immediately.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
