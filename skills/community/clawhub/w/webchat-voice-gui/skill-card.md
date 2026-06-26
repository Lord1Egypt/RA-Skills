## Description: <br>
Adds a microphone button and browser voice input controls to OpenClaw WebChat, using local MediaRecorder capture and a local faster-whisper transcription service to send transcribed text into chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neldar](https://clawhub.ai/user/neldar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw WebChat users and local developers use this skill to add push-to-talk, toggle recording, continuous transcription, and localized microphone controls to the WebChat Control UI. It is intended for local speech-to-text workflows that depend on an HTTPS WebChat proxy and a local faster-whisper backend. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently patches the OpenClaw WebChat Control UI and installs a user-level startup hook that can reapply the patch after updates. <br>
Mitigation: Review the modified Control UI paths and installed hook before use, run the included status check after deployment, and use the uninstall script to remove the hook and injected files when the voice UI is no longer needed. <br>
Risk: Continuous or live transcription can automatically submit spoken text into chat. <br>
Mitigation: Avoid enabling continuous transcription around sensitive conversations, prefer push-to-talk when manual control is needed, and review or edit captured text before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/neldar/webchat-voice-gui) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces install, verification, language-selection, and uninstall guidance for a local WebChat voice-input setup.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
