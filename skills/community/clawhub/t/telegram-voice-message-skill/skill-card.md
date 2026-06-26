## Description: <br>
Guides an AI assistant through generating, converting, validating, and sending Telegram voice messages in OGG/Opus format while avoiding common Telegram Bot API and TTS URL pitfalls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shynloc](https://clawhub.ai/user/shynloc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI automation builders use this skill to prepare TTS audio, convert it to Telegram-compatible OGG/Opus, and send it as a voice message instead of a generic audio file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Runnable examples and scripts include command-execution and automation patterns that require review before use. <br>
Mitigation: Review and harden the scripts, run them with least privilege, and start with test-only Telegram and TTS credentials. <br>
Risk: Telegram bot tokens and TTS API keys can be exposed through plaintext configuration, shell history, or debug output. <br>
Mitigation: Store credentials in environment variables or a secret manager, avoid committing filled configuration files, and keep debug logging disabled around secrets. <br>
Risk: Voice text and temporary audio files may contain sensitive content. <br>
Mitigation: Avoid sensitive text, restrict access to temporary files, clean generated audio promptly, and validate retention settings before deployment. <br>
Risk: Forwarding or exposing Telegram automation without authentication can leak messages or allow unauthorized sends. <br>
Mitigation: Require webhook authentication before exposing any server and disable cross-channel forwarding of original content unless it is explicitly reviewed. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/shynloc/telegram-voice-message-skill) <br>
- [Telegram voice guide](artifact/docs/telegram-voice-guide.md) <br>
- [Format requirements](artifact/docs/format-requirements.md) <br>
- [API integration guide](artifact/docs/api-integration.md) <br>
- [Best practices](artifact/docs/best-practices.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Bash scripts and JSON/Python configuration templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Telegram bot credentials, a TTS provider key, curl, ffmpeg, and careful handling of generated audio and temporary files.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
