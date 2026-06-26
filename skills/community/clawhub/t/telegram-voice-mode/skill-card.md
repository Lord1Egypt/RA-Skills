## Description: <br>
Toggles a voice reply mode that converts agent replies into Chinese voice messages and sends them through channels such as Telegram, while returning to text replies when disabled. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JianGuoPaPa](https://clawhub.ai/user/JianGuoPaPa) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and messaging automation developers use this skill to let an OpenClaw agent switch between text and voice replies, generate MP3 audio with edge-tts, and send voice messages to supported messaging channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The sender script can send generated voice messages to a hard-coded Telegram recipient when no destination is supplied. <br>
Mitigation: Remove or replace the default recipient, require an explicit destination for every send, and confirm the target before sending voice messages. <br>
Risk: Voice mode can route conversation content through the user's messaging account as generated audio. <br>
Mitigation: Use voice mode only for conversations appropriate for that messaging channel and avoid sensitive content until destination selection and confirmation are fixed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JianGuoPaPa/telegram-voice-mode) <br>
- [Publisher profile](https://clawhub.ai/user/JianGuoPaPa) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript helper scripts and plain-text command output; runtime helpers create MP3 audio files and can send voice messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Voice helpers default to zh-CN-XiaoxiaoNeural and write generated MP3 files under /tmp/voice-reply before optional message sending.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
