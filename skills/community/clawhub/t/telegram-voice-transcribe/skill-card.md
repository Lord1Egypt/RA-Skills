## Description: <br>
Transcribe Telegram voice messages and audio notes into text using the OpenAI Whisper API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dreadterror](https://clawhub.ai/user/dreadterror) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw agents use this skill to convert Telegram voice messages, Telegram audio notes, local audio files, or direct audio URLs into transcript text before responding to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default API workflow or hook can fetch Telegram audio with a bot token and upload private audio to OpenAI, while the documentation also describes local-private operation. <br>
Mitigation: Use --local when voice notes must remain on the server; otherwise inform users that Telegram audio may be fetched and sent to OpenAI before enabling automatic transcription. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dreadterror/telegram-voice-transcribe) <br>
- [Setup Guide](references/setup.md) <br>
- [Telegram Bot API](https://api.telegram.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON transcript output with Markdown setup and usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The transcript output may include language and duration fields, or an error field when transcription fails.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
