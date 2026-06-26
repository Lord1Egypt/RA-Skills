## Description: <br>
Deploy S-UI + Cloudflare WARP proxy server in one command. 6 protocols (VLESS Reality, TUIC, Hysteria2, gRPC, Trojan, WebSocket), clean Cloudflare IP exit via wireproxy (~54MB RAM). Use when the user wants to set up a proxy server, VPN alternative, or network tunnel on a VPS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ipythoning](https://clawhub.ai/user/ipythoning) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to deploy, audit, or troubleshoot a multi-protocol proxy or VPN-alternative server on a VPS using S-UI, sing-box, wireproxy, and Cloudflare WARP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Root-level one-line installation and broad persistent VPS changes can alter firewall, swap, services, and system configuration. <br>
Mitigation: Use only a disposable or dedicated VPS, review and pin the remote scripts before execution, and avoid hosts with other workloads or firewall and swap policies that must be preserved. <br>
Risk: The S-UI admin panel is exposed with default credentials after setup. <br>
Mitigation: Change the S-UI admin password before exposing the panel and restrict ports 2095 and 2096 with a firewall or VPN. <br>
Risk: Remote deployment over SSH can weaken host trust if password access or disabled host-key checks are used. <br>
Mitigation: Prefer SSH keys with host-key verification and confirm the target server before running deployment commands. <br>


## Reference(s): <br>
- [S-UI](https://github.com/alireza0/s-ui) <br>
- [sing-box](https://github.com/SagerNet/sing-box) <br>
- [wireproxy](https://github.com/pufferffish/wireproxy) <br>
- [wgcf](https://github.com/ViRb3/wgcf) <br>
- [ClawHub listing](https://clawhub.ai/ipythoning/suiwarp) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include VPS setup, verification, service management, and troubleshooting steps.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
