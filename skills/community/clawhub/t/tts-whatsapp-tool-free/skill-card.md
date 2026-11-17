## Description: <br>
WhatsApp语音消息免费版 helps personal users convert text into Piper TTS voice audio and send it as WhatsApp voice messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to generate a single WhatsApp-compatible voice message from text and send it to a specified recipient. It is intended for personal multilingual voice messaging, not certified translation or localization work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real WhatsApp voice messages to a configured or supplied recipient. <br>
Mitigation: Use it only after the user explicitly requests a WhatsApp voice message, verify the recipient and message content every time, and prefer --no-send preview before sending. <br>
Risk: The documented trigger scope includes ordinary translation and localization language, which is broader than the authority needed to send messages. <br>
Mitigation: Invoke this skill only for explicit text-to-speech WhatsApp message generation and route standalone translation or localization requests to a different workflow. <br>
Risk: Phone numbers, message text, and generated audio can contain sensitive personal information. <br>
Mitigation: Avoid hard-coded recipients, keep defaults in user-controlled configuration, minimize logs, and remove temporary audio after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/tts-whatsapp-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands, configuration examples, and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide the agent to generate OGG/Opus audio, send a WhatsApp voice message, and clean temporary files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
