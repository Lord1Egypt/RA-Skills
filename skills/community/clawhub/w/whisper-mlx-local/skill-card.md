## Description: <br>
Local Whisper provides local speech-to-text for Telegram and WhatsApp voice messages on Apple Silicon Macs using MLX Whisper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ImpKind](https://clawhub.ai/user/ImpKind) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to transcribe Telegram, WhatsApp, and other voice-message audio locally on Apple Silicon Macs instead of relying on paid transcription APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes local and private transcription claims while also including cloud transcription paths for OpenAI and Groq. <br>
Mitigation: Force a local backend for private use and avoid setting OpenAI or Groq credentials in the environment unless cloud transcription is intentional. <br>
Risk: The large-file helper has a code-injection risk when handling crafted filenames. <br>
Mitigation: Do not use the large-file helper on untrusted filenames until its path handling is fixed and reviewed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ImpKind/whisper-mlx-local) <br>
- [Source Repository](https://github.com/ImpKind/local-whisper) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text transcription output, JSON API responses, and Markdown setup guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS on Apple Silicon with Python 3.9+; the first local model download is about 1.5 GB.] <br>

## Skill Version(s): <br>
1.5.0 (source: release metadata and OpenClaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
