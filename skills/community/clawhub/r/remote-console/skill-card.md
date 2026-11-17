## Description:

Provides Python-scripted commands to start, stop, check, and validate a ttyd plus SSH tunnel remote console for accessing Claude Code or other CLI tools from a phone or browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haibaraaiaptx](https://clawhub.ai/user/haibaraaiaptx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to expose a configured project terminal through a browser-accessible remote console, mainly for mobile or tablet access to local CLI-based development workflows. It includes helper commands for launching, stopping, checking, and validating the remote console setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose a writable browser terminal for a host environment.

Mitigation: Use it only when that exposure is intentional, restrict access with VPN, firewall, loopback-only forwarding, or an authenticated proxy, and add TLS for browser access.

Risk: The bundled claude-bypass preset can launch an agent with permission checks disabled.

Mitigation: Remove the claude-bypass preset before use, or reserve it only for fully trusted private networks and non-sensitive personal projects.

Risk: Public SSH GatewayPorts exposure could make the remote console reachable beyond the intended audience.

Mitigation: Avoid public GatewayPorts exposure and prefer authenticated, limited network paths for the SSH tunnel.

Risk: The stop helper may not close every SSH tunnel instance in all configurations.

Mitigation: Verify after stopping that the ttyd and SSH tunnel processes are closed before assuming the console is offline.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/haibaraaiaptx/skills/remote-console)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run local Python helper scripts that start, stop, inspect, or validate ttyd and SSH tunnel processes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
