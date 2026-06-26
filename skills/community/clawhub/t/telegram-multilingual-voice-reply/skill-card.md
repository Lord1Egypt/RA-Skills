## Description: <br>
Smart Telegram reply workflow for OpenClaw: if the user sends text, reply with text; if the user sends a voice note/audio, transcribe locally using the installed mlx_audio (default Qwen3-ASR on Apple Silicon), then generate a meaningful reply in the same language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pengling9405](https://clawhub.ai/user/pengling9405) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to handle Telegram text and voice messages with language-following replies. Voice inputs are transcribed locally, answered in the detected or requested language, and can be returned as a single Telegram voice message with a matching caption. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram voice notes may contain sensitive content that is processed locally and may leave temporary audio or transcript files. <br>
Mitigation: Use the skill only when local processing is acceptable, keep the Python environment trusted, and periodically clear temporary files for sensitive conversations. <br>
Risk: The workflow can send Telegram replies on the user's behalf, including synthesized voice messages. <br>
Mitigation: Review generated reply text before sending when accuracy or tone matters, and keep the voice caption identical to the approved reply text. <br>
Risk: The helper scripts run mlx_audio and ffmpeg against user-provided audio and generated speech. <br>
Mitigation: Install dependencies from trusted sources and run the scripts in a controlled environment with the minimum file access needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pengling9405/telegram-multilingual-voice-reply) <br>
- [Qwen3-ASR notes](references/qwen3-asr-notes.md) <br>
- [mlx-audio Qwen3-ASR upstream README](https://github.com/Blaizzy/mlx-audio/blob/main/mlx_audio/stt/models/qwen3_asr/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with shell commands; helper scripts can emit plain text, JSON, SRT, VTT, and OGG/Opus voice files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Voice replies are intended to use one Telegram voice message whose caption matches the spoken reply text.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
