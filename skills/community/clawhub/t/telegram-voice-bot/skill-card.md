## Description: <br>
Telegram Voice Bot helps an agent run a Telegram bot that transcribes voice messages with Whisper and replies in Chinese using Microsoft Edge text-to-speech. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Polityang](https://clawhub.ai/user/Polityang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to configure and operate a Telegram voice bot that listens for voice messages, transcribes Chinese audio, and sends spoken replies. It is intended for bot deployment workflows where voice content and bot credentials are handled by the local runtime. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bot handles Telegram bot credentials and voice content. <br>
Mitigation: Use a dedicated Telegram bot token, keep it out of source control, disclose voice and transcript handling to chat participants, and avoid sensitive group chats unless automatic replies are acceptable. <br>
Risk: Dependencies are ambiguous or unpinned, including the Whisper package selection. <br>
Mitigation: Review and pin dependencies in an isolated environment before deployment, and verify that the intended Whisper package is installed. <br>
Risk: Automatic transcript and voice replies may expose recognized speech back into a chat. <br>
Mitigation: Limit deployment to chats where participants expect automatic transcription and spoken responses, or disable voice replies with the documented environment variable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Polityang/telegram-voice-bot) <br>
- [Publisher profile](https://clawhub.ai/user/Polityang) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup and runtime guidance for a Telegram bot that emits Telegram text or voice replies when executed.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
