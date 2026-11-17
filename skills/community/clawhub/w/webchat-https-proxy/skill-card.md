## Description:

HTTPS/WSS reverse proxy for the OpenClaw WebChat Control UI that serves the UI over HTTPS, proxies gateway WebSocket connections, forwards local transcription requests, manages self-signed TLS certificates, and runs as a user systemd service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neldar](https://clawhub.ai/user/neldar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to deploy and manage a local HTTPS/WSS proxy for the WebChat Control UI, gateway WebSocket traffic, and local transcription requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weak authentication can expose the local transcription service when LAN access is enabled.

Mitigation: Keep VOICE_HOST bound to 127.0.0.1 unless LAN exposure is required and understood; fix the authentication weakness before using the proxy on a shared network.

Risk: The skill creates a persistent user systemd service and changes OpenClaw allowed origins.

Mitigation: Review the deployment changes before installation and use the bundled uninstall script to remove the service, runtime file, certificates, and allowed origin when no longer needed.

Risk: Gateway tokens may be exposed if placed in URLs or shell commands that can be logged.

Mitigation: Avoid passing gateway tokens in URLs or command histories; prefer safer token handling appropriate for the deployment environment.

## Reference(s):

- [WebChat HTTPS Proxy on ClawHub](https://clawhub.ai/neldar/skills/webchat-https-proxy)
- [Troubleshooting - HTTPS Proxy](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell commands and configuration paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes deployment, status, uninstall, and troubleshooting guidance.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
