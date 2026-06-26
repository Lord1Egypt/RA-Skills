## Description: <br>
Sends text-to-speech voice messages to specified Telegram groups and topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sanwecn](https://clawhub.ai/user/sanwecn) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to generate Chinese TTS audio, convert it to Telegram-compatible OGG Opus voice format, and send it into a target Telegram group or topic. It is suited to community notifications, topic-specific updates, and organized group workflows that need spoken summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documentation asks for broader Telegram administrator permissions than are needed to send voice messages. <br>
Mitigation: Grant only the minimum Telegram bot permissions needed to send messages and media in the intended groups or topics. <br>
Risk: The security evidence reports unsafe command execution paths. <br>
Mitigation: Use only with trusted users or agents until the command-execution issue is fixed and re-scanned. <br>
Risk: Voice messages may expose sensitive or private information to Telegram group members. <br>
Mitigation: Do not send secrets or private information through this skill, and restrict target groups and topics to the intended audience. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sanwecn/telegram-voice-group) <br>
- [Publisher profile](https://clawhub.ai/user/sanwecn) <br>
- [README](artifact/README.md) <br>
- [Dependency guide](artifact/DEPENDENCIES.md) <br>
- [Feature details](artifact/FEATURES.md) <br>
- [Telegram topic guide](artifact/TELEGRAM_TOPICS.md) <br>
- [Use cases](artifact/USE_CASES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and shell command examples; runtime behavior sends Telegram voice messages as OGG Opus audio.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Linux, edge-tts, ffmpeg, Telegram bot send-message/send-media permissions, and OpenClaw messaging support.] <br>

## Skill Version(s): <br>
0.1.5 (source: ClawHub release evidence; package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
