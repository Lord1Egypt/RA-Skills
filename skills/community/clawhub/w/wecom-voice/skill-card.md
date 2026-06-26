## Description: <br>
Send native voice messages to WeCom using Windows TTS. Converts text to speech and sends as voice message (not audio file). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fanqisyx](https://clawhub.ai/user/fanqisyx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators using OpenClaw with WeCom use this skill to convert text into native voice-message media and send it to a selected WeCom recipient from a Windows environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real WeCom voice messages, including to a default recipient if no recipient is supplied. <br>
Mitigation: Use only trusted, controlled inputs and confirm the recipient explicitly before execution. <br>
Risk: The script builds local PowerShell and shell commands from user-provided text. <br>
Mitigation: Review before installing or running; prefer an implementation that escapes PowerShell content and uses argument-array process execution. <br>
Risk: Generated media may contain sensitive dictated content and can remain on disk after sending. <br>
Mitigation: Avoid sensitive text unless required and clean up generated WAV and AMR files after delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fanqisyx/wecom-voice) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, API Calls, Guidance] <br>
**Output Format:** [Command-line execution that generates WAV and AMR media files and sends a WeCom voice message.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Windows System.Speech, FFmpeg, OpenClaw, and access to the local OpenClaw media directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
