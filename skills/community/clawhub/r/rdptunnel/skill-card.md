## Description: <br>
Rdptunnel provides instructions for exposing local RDP servers over an aitun TCP tunnel using the AITUN/1 plain-TCP handshake. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ctz168](https://clawhub.ai/user/ctz168) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, support teams, and operators use this skill to make a Windows RDP server, Linux xrdp host, or GUI server reachable when it is behind NAT, a firewall, or a private network. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose a powerful remote desktop service to the public internet through a tunnel. <br>
Mitigation: Use it only for deliberate, temporary access to machines you control; prefer VPN, bastion, or IP-restricted access when possible; require strong unique credentials, Network Level Authentication, restricted users, monitoring, and disable the tunnel and RDP or xrdp when finished. <br>
Risk: The documented curl-to-bash and PowerShell irm-to-iex installation shortcuts execute remote installer content. <br>
Mitigation: Prefer package-manager installation or independently verify the installer before using those shortcuts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ctz168/skills/rdptunnel) <br>
- [AiTun Homepage](https://aitun.cc) <br>
- [ClawHub Package Metadata](https://clawhub.ai/ctz168/rdptunnel) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash and PowerShell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes installation, RDP service setup, tunnel creation, remote connection, cleanup, and security guidance for aitun-based RDP access.] <br>

## Skill Version(s): <br>
4.9.23 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
