## Description: <br>
Deprecated skill that installs a local HTTPS/WSS proxy and browser voice-input UI for OpenClaw WebChat, forwarding microphone audio to a local faster-whisper transcription service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neldar](https://clawhub.ai/user/neldar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this deprecated skill to add microphone controls, local transcription, and an HTTPS/WSS proxy to WebChat when they still need the legacy combined deployment. The author recommends newer split skills for modular deployments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs a persistent local HTTPS/WSS proxy, startup hook, and UI injection for OpenClaw WebChat. <br>
Mitigation: Review the listed modified paths before deployment and use the uninstall script when the service, hook, or UI changes are no longer needed. <br>
Risk: Changing the bind host from the localhost default can expose the proxy, gateway WebSocket path, and transcription endpoint on a LAN. <br>
Mitigation: Keep the service bound to 127.0.0.1 unless LAN access is required, and only expose it on trusted networks. <br>
Risk: Microphone audio is sent to a local transcription endpoint and URLs may contain gateway tokens. <br>
Mitigation: Run the transcription service locally as documented, avoid sharing token-bearing URLs, and rely on the token-authenticated transcription path described in the security evidence. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/neldar/webchat-voice-proxy) <br>
- [neldar Publisher Profile](https://clawhub.ai/user/neldar) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration paths, and deployment instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local setup and troubleshooting guidance for OpenClaw voice input; no external hosted output is claimed.] <br>

## Skill Version(s): <br>
0.2.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
