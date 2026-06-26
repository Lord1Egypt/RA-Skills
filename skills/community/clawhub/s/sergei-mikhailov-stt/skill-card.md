## Description: <br>
Speech recognition from voice messages using Yandex SpeechKit, with an extensible architecture for other providers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bzSega](https://clawhub.ai/user/bzSega) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill in OpenClaw to transcribe voice messages or local audio files into text through Yandex SpeechKit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio selected for transcription is sent to Yandex SpeechKit for processing. <br>
Mitigation: Install and use the skill only for audio that may be processed by Yandex SpeechKit. <br>
Risk: Yandex credentials are required for operation. <br>
Mitigation: Use a least-privilege Yandex service account key and store credentials in OpenClaw configuration rather than chat, logs, or shared diagnostics. <br>
Risk: The skill depends on local Python packages, FFmpeg, and an owner-controlled temporary directory. <br>
Mitigation: Keep Python dependencies and FFmpeg current, and ensure the configured temporary directory is controlled by the skill owner. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bzSega/sergei-mikhailov-stt) <br>
- [Yandex Cloud documentation](https://yandex.cloud/ru/docs) <br>
- [OpenClaw documentation](https://docs.openclaw.ai/) <br>
- [OpenClaw skills configuration](https://docs.openclaw.ai/tools/skills-config) <br>
- [FFmpeg downloads](https://ffmpeg.org/download.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown with optional JSON metadata and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Successful transcription can include recognized text, language, confidence, provider, and processing time.] <br>

## Skill Version(s): <br>
1.1.8 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
