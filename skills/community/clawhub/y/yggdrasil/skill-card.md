## Description: <br>
Diagnose Yggdrasil installation and daemon status for IPv6 P2P connectivity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jing-yilin](https://clawhub.ai/user/Jing-yilin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to check whether Yggdrasil is installed, running, and producing a routable IPv6 address for OpenClaw P2P connectivity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Yggdrasil setup may require elevated networking privileges or container TUN access. <br>
Mitigation: Grant only the needed CAP_NET_ADMIN or /dev/net/tun access, restart the OpenClaw gateway, and confirm status with yggdrasil_check. <br>
Risk: Authenticated registry or moderation actions may be available when privileged credentials are configured. <br>
Mitigation: Use least-privilege credentials and avoid staff-level tools unless they are required for the target environment. <br>


## Reference(s): <br>
- [Yggdrasil Installation Guide](references/install.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Jing-yilin/yggdrasil) <br>
- [OpenClaw Homepage](https://github.com/ReScienceLab/declaw) <br>
- [Yggdrasil Release Downloads](https://github.com/yggdrasil-network/yggdrasil-go/releases/latest) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Explains yggdrasil_check results and install or restart steps.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata; artifact frontmatter says 0.1.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
