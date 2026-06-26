## Description: <br>
Manages and uses a local ssh-agentd service for systemd persistence, API calls, connectivity checks, and session or metrics troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[offlinecat-dev](https://clawhub.ai/user/offlinecat-dev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to manage a known local ssh-agentd deployment, call its localhost API, and troubleshoot service state, sessions, metrics, and SSH connectivity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent ssh-agentd service control and remote-command execution can affect local and remote systems if used in the wrong environment. <br>
Mitigation: Install only for the intended local ssh-agentd setup and require explicit approval before enabling autostart, restarting or stopping the service, or calling /run. <br>
Risk: Incorrect daemon, token, host, or localhost binding configuration can expose or break SSH automation. <br>
Mitigation: Verify the daemon path, systemd unit, hosts.yaml, token handling, localhost binding, service status, health endpoint, and sessions before operational use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/offlinecat-dev/ssh-agentd-control) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline bash code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are intended for a specific local ssh-agentd setup and may require elevated privileges or a bearer token.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
