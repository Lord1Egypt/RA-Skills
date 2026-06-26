## Description: <br>
Voice Mode lets an agent convert Telegram text replies into Chinese voice messages with edge-tts when voice mode is enabled. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yl11023](https://clawhub.ai/user/yl11023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add Telegram voice-message delivery after normal text replies. It is intended for environments where edge-tts, Telegram bot access, and the voice-mode toggle file are deliberately configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release hardcodes a Telegram bot token, chat ID, and local path that could send reply content to an unintended account. <br>
Mitigation: Replace the token, chat ID, and path with controlled configuration before use, and rotate the exposed bot token. <br>
Risk: The included daemon can run as a long-lived Telegram polling process when invoked. <br>
Mitigation: Run the daemon only when that behavior is intended and the Telegram bot and chat are fully controlled. <br>


## Reference(s): <br>
- [Voice Mode on ClawHub](https://clawhub.ai/yl11023/voice-mode) <br>
- [yl11023 publisher profile](https://clawhub.ai/user/yl11023) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown instructions with inline PowerShell and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a .voice-mode toggle file, generate an MP3 voice file, and send Telegram voice messages when configured and enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
