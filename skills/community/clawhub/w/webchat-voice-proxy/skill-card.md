## Description:

Deprecated skill that deploys an OpenClaw WebChat HTTPS/WSS voice proxy with local transcription, mic button UI injection, keyboard controls, and localization, superseded by split replacement skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neldar](https://clawhub.ai/user/neldar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add voice input to OpenClaw WebChat by deploying a local HTTPS/WSS proxy, injecting a microphone UI, and routing audio to a local faster-whisper transcription service. The release is deprecated and points users to split replacement skills for new installations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The proxy handles microphone audio and forwards transcriptions into chat.

Mitigation: Review the bundled scripts before installation and prefer the newer split replacement skills for new deployments.

Risk: LAN exposure can make the HTTPS proxy, gateway WebSocket path, and transcription endpoint reachable by other devices on the network.

Mitigation: Keep the proxy bound to 127.0.0.1 unless LAN access is explicitly required, and do not expose it without reliable authentication.

Risk: Gateway token handling is part of the transcription and WebSocket flow.

Mitigation: Verify token and pairing behavior after deployment, and avoid custom HTTPS ports unless the endpoint bug noted in security guidance is fixed.

Risk: Continuous mode can send transcribed speech into chat automatically after a short review period.

Mitigation: Use push-to-talk for sensitive sessions and review continuous-mode behavior before enabling it.

Risk: The skill creates persistent local changes, including a user systemd service and gateway startup hook.

Mitigation: Use the bundled uninstall script to remove the service, hook, injected UI asset, allowed origin, certificates, and workspace files when no longer needed.

## Reference(s):

- [WebChat Voice Proxy ClawHub Page](https://clawhub.ai/neldar/skills/webchat-voice-proxy)
- [Troubleshooting](artifact/references/troubleshooting.md)
- [Security Audit](artifact/SECURITY-AUDIT.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Code, Guidance]

**Output Format:** [Markdown instructions with inline shell commands, configuration paths, and bundled scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local deployment guidance and scripts that modify OpenClaw Control UI assets, gateway configuration, a user systemd service, and a startup hook.]

## Skill Version(s):

0.2.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
