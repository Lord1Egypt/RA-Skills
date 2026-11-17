## Description:

Launch, stop, restart, or check the status of a remote Chrome browser service using Xvfb, x11vnc, and noVNC.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kelvinschen](https://clawhub.ai/user/kelvinschen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to start, stop, restart, and inspect a remotely accessible Chrome GUI for browser automation, visual verification, and debugging through noVNC, VNC, and Chrome DevTools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote Chrome, VNC, and noVNC access can expose browser control if ports 5900, 6080, or 9222 are reachable from untrusted networks.

Mitigation: Install only on isolated or trusted hosts, prefer localhost binding, and use SSH or VPN tunneling instead of exposing these ports publicly.

Risk: The start and status flows can print VNC passwords and noVNC URLs that grant browser access.

Mitigation: Treat generated passwords and URLs as secrets and avoid sharing terminal output or logs that contain them.

Risk: The security guidance identifies password storage and process cleanup as areas needing hardening before elevated use.

Mitigation: Avoid running the scripts as root and review password handling and service cleanup behavior before deployment.

## Reference(s):

- [Installation Guide](references/installation.md)
- [Configuration Reference](references/configuration.md)
- [Output Format Examples](references/output-examples.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and terminal output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes generated noVNC/VNC access details, VNC password output, process status, memory usage, open tabs, and service control guidance when the scripts are run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
