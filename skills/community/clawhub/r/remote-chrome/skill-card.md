## Description: <br>
Launch, stop, restart, or check the status of a remote Chrome browser service using Xvfb, x11vnc, and noVNC for GUI access through a web browser or VNC client. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kelvinschen](https://clawhub.ai/user/kelvinschen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run and manage a remotely accessible Chrome GUI for browser testing, visual inspection, or agent-assisted browser automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes a live browser session through VNC and noVNC access. <br>
Mitigation: Use it only when a remotely controllable Chrome session is intentional, keep access on localhost or behind SSH tunnels, VPNs, or strict firewall allowlists, and stop the service when finished. <br>
Risk: The noVNC URL and VNC password grant access to the browser session if shared. <br>
Mitigation: Treat generated URLs, passwords, status output, and screenshots as secrets and avoid posting or logging them in shared locations. <br>
Risk: Chrome remote debugging access can allow control of the browser session. <br>
Mitigation: Keep the debugging port off the public internet and restrict access to trusted local or tunneled connections. <br>


## Reference(s): <br>
- [Installation Guide](references/installation.md) <br>
- [Output Format Examples](references/output-examples.md) <br>
- [Configuration Reference](references/configuration.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and service access details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational commands and status details for local shell execution; running the scripts may expose access URLs and credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
