## Description: <br>
Qwen Omni Multimodal calls Alibaba Cloud DashScope Qwen3.5-Omni models for text, image, audio, and video understanding with text or speech output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouweico](https://clawhub.ai/user/zhouweico) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill to send selected prompts, images, audio, and video to DashScope Qwen-Omni for multimodal question answering, transcription, summarization, and speech response generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected prompts, images, audio, and video are sent to Alibaba Cloud DashScope for processing. <br>
Mitigation: Use this skill only when that external processing is acceptable for the data; verify the configured base URL before running requests. <br>
Risk: API credentials may be exposed if stored in local configuration files. <br>
Mitigation: Prefer DASHSCOPE_API_KEY from an environment variable or secret manager and keep any config.json private. <br>
Risk: Saved sessions can retain private prompts or media-derived context on disk. <br>
Mitigation: Use single-turn or dry-run mode for sensitive work, and clear saved sessions when they may contain private material. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/zhouweico/qwen-omni-multimodal) <br>
- [Qwen-Omni API Notes](references/api.md) <br>
- [Alibaba Cloud Qwen-Omni documentation](https://help.aliyun.com/zh/model-studio/qwen-omni) <br>
- [Alibaba Cloud Qwen API calling guide](https://help.aliyun.com/zh/model-studio/developer-reference/use-qwen-by-calling-api) <br>
- [Alibaba Cloud streaming documentation](https://help.aliyun.com/zh/model-studio/stream) <br>


## Skill Output: <br>
**Output Type(s):** [text, audio files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; runtime responses are streamed text and optional WAV audio files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18 or newer and DASHSCOPE_API_KEY; dry-run mode previews requests without calling the API.] <br>

## Skill Version(s): <br>
0.2.0 (source: release evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
