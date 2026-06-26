## Description: <br>
Transcribes Telegram voice-message audio through the Yandex SpeechKit API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[strydex](https://clawhub.ai/user/strydex) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to convert Telegram voice messages or supported audio files into text via Yandex SpeechKit. It can be used from the command line or imported as Python helper code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio and derived transcripts are sent to Yandex SpeechKit for processing. <br>
Mitigation: Use only with audio that is approved for third-party transcription, and confirm data-handling requirements before deployment. <br>
Risk: Yandex service-account credentials may be stored locally in config.json. <br>
Mitigation: Protect the configuration file with restrictive permissions or a secret manager, and rotate credentials if exposure is suspected. <br>
Risk: The helper script can continuously process inbound voice files and forward transcripts to a hard-coded Telegram recipient. <br>
Mitigation: Do not run scripts/voice_processor.py until the recipient is configurable, monitored files are restricted or approved, and transcript storage in the workspace is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/strydex/yandex-speechkit-stt) <br>
- [Publisher profile](https://clawhub.ai/user/strydex) <br>
- [Yandex IAM token endpoint](https://iam.api.cloud.yandex.net/iam/v1/tokens) <br>
- [Yandex SpeechKit STT recognize endpoint](https://stt.api.cloud.yandex.net/speech/v1/stt:recognize) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, configuration, guidance] <br>
**Output Format:** [Plain text transcription output with Markdown setup and usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, ffmpeg, and Python packages PyJWT, cryptography, and requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
