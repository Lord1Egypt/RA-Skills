## Description: <br>
小野语音系统 generates speech audio from text using local macOS Chinese voice support and Edge-TTS for other languages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackytianjp](https://clawhub.ai/user/jackytianjp) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to turn Chinese, English, Japanese, or French text into voice audio for assistants, Telegram bots, and OpenClaw-style integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Non-Chinese text is processed through Microsoft Edge-TTS cloud service. <br>
Mitigation: Use non-sensitive text for cloud-routed languages and review data-handling expectations before deployment. <br>
Risk: Generated audio remains on disk under the OpenClaw outputs folder. <br>
Mitigation: Delete generated audio when it is no longer needed and manage file retention according to the deployment environment. <br>
Risk: The skill depends on ffmpeg and optional Edge-TTS installation for full functionality. <br>
Mitigation: Install ffmpeg and edge-tts from trusted sources and keep them updated. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jackytianjp/xiaoye-voice) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Audio files in OGG, MP3, or WAV format with generated file paths and status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes generated audio under the user's OpenClaw outputs folder by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
