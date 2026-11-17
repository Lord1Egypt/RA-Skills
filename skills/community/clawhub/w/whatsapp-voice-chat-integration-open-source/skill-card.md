## Description:

Processes WhatsApp voice notes by transcribing audio with Whisper, detecting English and Hindi intents, executing handlers, and returning responses for conversational WhatsApp bots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[syedateebulislam](https://clawhub.ai/user/syedateebulislam)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation builders use this skill to add WhatsApp voice-note transcription, intent detection, and response handling to Clawdbot-style conversational assistants. It is suited to opted-in voice assistants, multilingual chatbots, and controlled command interfaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command execution and temporary audio-file handling may expose real WhatsApp messages or increase local execution risk.

Mitigation: Review and patch command invocation and temp-file handling before use, restrict the inbound directory and process privileges, and install reviewed pinned dependencies.

Risk: Voice transcripts, sender identifiers, and responses can contain sensitive personal data.

Mitigation: Run the listener only for opted-in users, minimize transcript and response logging, and protect processed-message logs.

Risk: Custom intent handlers can trigger external APIs or physical-device actions from imperfect voice intent matches.

Mitigation: Require sender verification, allowlists, and explicit confirmation before device control or other consequential actions.

## Reference(s):

- [WhatsApp Voice Talk - Setup Guide](artifact/references/SETUP.md)
- [WhatsApp Voice Talk - API Reference](artifact/references/API.md)
- [ClawHub skill page](https://clawhub.ai/syedateebulislam/skills/whatsapp-voice-chat-integration-open-source)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript, Python, shell command, and JSON examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documented API results include status, response, transcript, intent, language, sender, timestamp, and error fields.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
