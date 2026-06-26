## Description: <br>
Smart Voice Reply helps an agent synthesize voice replies with selectable voice profiles and configure voice-tone instructions for user-requested scenarios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[slbqc](https://clawhub.ai/user/slbqc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate spoken replies through DashScope text-to-speech, send generated audio through OpenClaw, and maintain reusable voice-profile instructions for common or custom scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup instructions can persistently change future agent behavior by adding voice-reply rules to USER.md. <br>
Mitigation: Review USER.md edits before applying them and avoid enabling always-on voice replies unless that behavior is explicitly desired. <br>
Risk: Reply text and audio metadata may be stored locally and sent to DashScope during synthesis. <br>
Mitigation: Avoid synthesizing sensitive text and keep generated request, response, and audio files in an appropriate workspace-controlled output directory. <br>
Risk: The skill requires DASHSCOPE_API_KEY for outbound API calls. <br>
Mitigation: Store DASHSCOPE_API_KEY only in environment or secret storage and do not hard-code it in skill files or user configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/slbqc/smart-voice-reply) <br>
- [Publisher profile](https://clawhub.ai/user/slbqc) <br>
- [DashScope multimodal generation endpoint](https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation) <br>
- [Skill installation guide](artifact/docs/技能安装配置指导.md) <br>
- [Voice instruction guide](artifact/docs/音色指令创建指导.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated audio file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DASHSCOPE_API_KEY and writes request, response, and audio files under the configured output directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
