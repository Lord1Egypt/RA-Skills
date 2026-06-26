## Description: <br>
Voice Log starts and stops background voice journaling, streams microphone audio to Soniox realtime speech-to-text while running, and returns recent rolling transcript text for summarization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[easwee](https://clawhub.ai/user/easwee) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to deliberately start or stop a local voice journal, check recording status, and summarize recent conversation from the rolling transcript. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Microphone recording and transcription can capture sensitive or non-consenting conversation. <br>
Mitigation: Start recording deliberately, stop it when finished, check status if unsure, and avoid recording sensitive or non-consenting conversations. <br>
Risk: The Soniox API key enables access to the transcription service if exposed. <br>
Mitigation: Use a revocable Soniox API key and rotate or revoke it if it may have been exposed. <br>
Risk: The local rolling transcript may contain private conversation text. <br>
Mitigation: Run the skill only on trusted devices and accounts; the skill stores transcript data under its local `.data` directory with best-effort restrictive permissions. <br>


## Reference(s): <br>
- [Voice Log on ClawHub](https://clawhub.ai/easwee/voice-log) <br>
- [easwee publisher profile](https://clawhub.ai/user/easwee) <br>
- [Soniox Speech-to-Text](https://soniox.com/speech-to-text) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Short natural-language responses, transcript text, JSON status output, and inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The rolling transcript keeps the latest 60 minutes; the `last` command returns up to 1800 characters by default unless overridden.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release evidence, package.json, skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
