## Description: <br>
Real-time WhatsApp voice message processing that transcribes voice notes with Whisper, detects intent, executes handlers, and sends responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[syedateebulislam](https://clawhub.ai/user/syedateebulislam) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to add WhatsApp voice-note workflows to agents, including transcription, intent matching, and response generation for English and Hindi voice interactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private voice messages and transcripts may be exposed through logs or retained processing artifacts. <br>
Mitigation: Disable raw transcript logging, protect operational logs, and run the listener only for trusted WhatsApp senders. <br>
Risk: Shell-string execution with an audio path can be unsafe if file paths are not controlled. <br>
Mitigation: Replace shell-string execSync usage with argument-safe process execution before deployment. <br>
Risk: Custom handlers can affect devices, accounts, files, or public outputs when connected to real integrations. <br>
Mitigation: Require explicit review and confirmation before enabling handlers that perform external actions. <br>
Risk: The long-running listener continuously processes new inbound media. <br>
Mitigation: Run it with least privilege, monitor its logs, and restrict watched directories and allowed senders. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/syedateebulislam/whatsapp-voice-chat-integration-open-source) <br>
- [API Reference](references/API.md) <br>
- [Setup Guide](references/SETUP.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, JavaScript and Python code examples, shell commands, and JSON-like processing results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces transcripts, detected intent labels, language codes, response text, and status/error fields for voice-message processing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
