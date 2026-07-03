## Description: <br>
VPN Tunnel helps an agent start a WireGuard tunnel and local SOCKS5 proxy through a cloud VPS for blocked international websites, then close the tunnel after use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smile113311](https://clawhub.ai/user/smile113311) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create an on-demand proxy path for overseas or blocked sites such as Google, Docker Hub, and other APIs when direct access fails. It also provides commands to check tunnel status and shut the tunnel down immediately after use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill embeds credentials and uses automated privileged network commands. <br>
Mitigation: Install only when you control the VPS and host setup; rotate exposed credentials, replace hardcoded passwords with interactive sudo or a secret manager, and use SSH keys instead of sshpass. <br>
Risk: The tunnel can route requests through an external VPS and may remain active if not closed. <br>
Mitigation: Require explicit confirmation before starting the tunnel, use it only for blocked international sites, and run the shutdown command immediately after the task completes. <br>
Risk: Connectivity tests contact external services and reveal the proxy exit path. <br>
Mitigation: Keep external connectivity tests opt-in and review the target URLs before running them. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/smile113311/vpn-tunnel) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local WireGuard, sudo access, sshpass, SSH connectivity to the configured VPS, and SOCKS5 proxy use on 127.0.0.1:1080.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
