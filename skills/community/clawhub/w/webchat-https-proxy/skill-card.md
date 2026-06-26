## Description: <br>
HTTPS/WSS reverse proxy for OpenClaw WebChat Control UI that serves the Control UI over HTTPS, manages TLS certificates, proxies WebSocket connections to the gateway, and forwards /transcribe requests to the local faster-whisper endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neldar](https://clawhub.ai/user/neldar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to deploy and manage a local HTTPS/WSS proxy for OpenClaw WebChat Control UI, including TLS setup, gateway origin configuration, WebSocket proxying, and transcription request forwarding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs an always-on user-level HTTPS/WSS proxy service for OpenClaw WebChat. <br>
Mitigation: Install it only when a persistent local proxy is needed, and remove or disable the user service with uninstall.sh or systemctl --user disable --now openclaw-voice-https.service when it is no longer required. <br>
Risk: LAN exposure can make the proxy reachable beyond localhost if the bind host is changed. <br>
Mitigation: Keep the default localhost binding unless trusted LAN access is intentional, and review VOICE_HOST and VOICE_ALLOWED_ORIGIN before redeploying. <br>
Risk: Gateway tokens may appear in URLs, logs, screenshots, or shell history during setup and troubleshooting. <br>
Mitigation: Avoid sharing URLs, logs, screenshots, or command history that contain gateway tokens. <br>


## Reference(s): <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/neldar/webchat-https-proxy) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces user-level systemd service setup, local proxy runtime files, TLS certificate paths, status checks, and uninstall guidance.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
