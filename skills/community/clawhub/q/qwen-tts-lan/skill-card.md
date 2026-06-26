## Description: <br>
Qwen Tts helps agents convert text into natural speech with Alibaba Cloud Qwen TTS, including voice selection and optional Feishu delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanlan314](https://clawhub.ai/user/lanlan314) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to synthesize text into audio with Qwen TTS, choose supported voices and languages, and optionally send generated audio to a configured Feishu recipient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for synthesis is sent to Alibaba DashScope. <br>
Mitigation: Avoid sending sensitive text unless that data sharing is acceptable for the intended use case. <br>
Risk: The Feishu helper uploads and sends generated audio to the configured Feishu user. <br>
Mitigation: Use the Feishu send script only when delivery is intentional, keep credentials scoped, and verify FEISHU_USER_ID before use. <br>
Risk: Voice cloning or custom voice workflows can reproduce a person's voice. <br>
Mitigation: Use voice cloning only with clear permission from the voice owner. <br>


## Reference(s): <br>
- [Qwen Tts ClawHub release](https://clawhub.ai/lanlan314/qwen-tts-lan) <br>
- [Qwen TTS API Reference](references/api.md) <br>
- [Qwen TTS Voice List](references/voices.md) <br>
- [Alibaba Cloud DashScope Console](https://dashscope.console.aliyun.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell and Python usage examples; scripts can produce local OGG audio files or Feishu send results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DASHSCOPE_API_KEY for synthesis; Feishu delivery also requires FEISHU_APP_ID, FEISHU_APP_SECRET, and FEISHU_USER_ID.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
