## Description:

Bailian TTS helps agents generate Chinese and multilingual speech audio with Alibaba Bailian/DashScope Qwen TTS models, selectable voices, and file output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dadaniya99](https://clawhub.ai/user/dadaniya99)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert supplied text into speech audio through Bailian/DashScope TTS models, choose supported voices, and save the resulting audio file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud TTS requests may expose submitted text or sensitive data to an external service.

Mitigation: Avoid sending secrets or regulated personal data, and follow the evidence guidance to run the skill in an isolated environment.

Risk: The script writes downloaded audio to a user-selected output path.

Mitigation: Choose output paths deliberately and avoid overwriting important files.

Risk: The skill requires a DashScope API key.

Mitigation: Protect the API key, prefer environment-based secret handling, and avoid committing credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dadaniya99/skills/xiaolongxia-bailian-tts)
- [Qwen TTS official documentation](https://help.aliyun.com/zh/model-studio/qwen-tts)
- [Qwen TTS voice cloning documentation](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-cloning)
- [Qwen TTS voice design documentation](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-design)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration guidance, Files]

**Output Format:** [Markdown guidance with Python and shell examples; generated audio is written as an Opus file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a DashScope API key and network access to the cloud TTS service.]

## Skill Version(s):

1.2.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
