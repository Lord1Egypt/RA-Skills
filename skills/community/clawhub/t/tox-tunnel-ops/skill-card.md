## Description: <br>
Tox Tunnel Ops helps agents design, deploy, and troubleshoot encrypted P2P TCP tunnels for SSH, RDP/VNC, databases, web apps, homelab services, loopback SOCKS5/HTTP CONNECT access, and Prometheus/Grafana monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anonymoussoft](https://clawhub.ai/user/anonymoussoft) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and administrators use this skill to generate ToxTunnel client, server, and rules YAML, install or run the toxtunnel binary, diagnose tunnel failures, and verify scoped remote access to internal services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports remote-access tunnels for sensitive services such as RDP, NAS, databases, and admin web interfaces. <br>
Mitigation: Limit rules to exact friend keys, hosts, and ports; keep access time-scoped; revoke temporary access after the maintenance window. <br>
Risk: Installer workflows may pipe remote scripts into privileged shells. <br>
Mitigation: Prefer verified release packages or review installer scripts before running them with administrator privileges. <br>
Risk: Generated service files, file paths, and daemon changes can affect persistent host access. <br>
Mitigation: Confirm every generated path, system service change, and startup command before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/anonymoussoft/tox-tunnel-ops) <br>
- [tox-tcp-tunnel Project Homepage](https://github.com/anonymoussoft/tox-tcp-tunnel) <br>
- [Diagnose Reference](references/diagnose.md) <br>
- [Execute Reference](references/execute.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with YAML configuration snippets and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated ToxTunnel client, server, and rules YAML plus diagnostic or verification steps.] <br>

## Skill Version(s): <br>
0.4.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
