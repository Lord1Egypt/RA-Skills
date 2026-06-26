## Description: <br>
Automatically converts speech messages in ogg, wav, mp3, and m4a formats to text using offline Faster-Whisper with ffmpeg format conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lqwall26](https://clawhub.ai/user/lqwall26) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to transcribe local voice-message attachments into text so the agent can continue a conversation from spoken input. It is primarily configured for Chinese speech recognition and local processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local voice messages may be converted and transcribed into agent-readable text. <br>
Mitigation: Install and use the skill only where users are comfortable exposing the selected local audio file contents to the agent workflow. <br>
Risk: Manual use without an attachment may process the newest inbound voice file. <br>
Mitigation: Provide an explicit voice-file attachment or path when possible, and review the returned file path before relying on the transcript. <br>
Risk: Audio conversion depends on ffmpeg and Python packages from the local environment. <br>
Mitigation: Install ffmpeg, faster-whisper, and pydub from trusted sources and keep the system PATH pointed at the intended ffmpeg installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lqwall26/speech2text) <br>
- [Publisher profile](https://clawhub.ai/user/lqwall26) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, shell commands, guidance] <br>
**Output Format:** [Text result with JSON-style success or error fields, plus Markdown installation and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local Faster-Whisper model, ffmpeg conversion, default Chinese language recognition, and a tiny model size unless changed by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
