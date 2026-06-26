## Description: <br>
Auto-transcribes Telegram voice messages in .ogg Opus format to text using a local OpenAI Whisper tiny model, replies with the transcription, and removes local audio files for privacy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drones277](https://clawhub.ai/user/drones277) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to automatically transcribe inbound Telegram voice messages locally and send the resulting text as a reply without relying on external transcription APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic replies may send an incorrect or incomplete transcription. <br>
Mitigation: Review the workflow before enabling unattended use and use a larger Whisper model when higher transcription accuracy is needed. <br>
Risk: Cleanup commands may remove source audio or temporary transcript files before the reply has been sent successfully. <br>
Mitigation: Confirm the watched path and adjust cleanup so files are removed only after successful transcription and message delivery. <br>
Risk: A cron or sub-agent loop can keep processing messages until explicitly disabled. <br>
Mitigation: Keep a clear disable path for the background job and confirm the polling target before enabling it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/drones277/tg-voice-whisper) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces transcription workflow guidance for local Whisper execution, Telegram reply actions, cleanup, and optional background automation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
