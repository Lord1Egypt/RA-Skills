## Description: <br>
Send high-quality text-to-speech voice messages on WhatsApp in 40+ languages with automatic delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hopyky](https://clawhub.ai/user/hopyky) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to generate multilingual Piper text-to-speech audio and send it as WhatsApp voice messages to individual contacts or groups through Clawdbot. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real WhatsApp messages through the connected Clawdbot account. <br>
Mitigation: Install only when the connected WhatsApp account is trusted, test first with --no-send, and verify recipients or group IDs before sending. <br>
Risk: A configured default recipient can cause generated voice messages to be delivered automatically to that contact or group. <br>
Mitigation: Avoid setting WHATSAPP_DEFAULT_TARGET unless automatic delivery to that recipient is intended. <br>
Risk: The skill depends on externally downloaded voice models and related tooling. <br>
Mitigation: Review external downloads or cloned code before running them. <br>


## Reference(s): <br>
- [TTS WhatsApp on ClawHub](https://clawhub.ai/hopyky/tts-whatsapp) <br>
- [Piper Voice Samples](https://rhasspy.github.io/piper-samples/) <br>
- [Piper voices on Hugging Face](https://huggingface.co/rhasspy/piper-voices) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces WhatsApp-ready OGG/Opus voice-message guidance; generated audio may be sent automatically unless --no-send is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, CHANGELOG released 2026-01-22) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
