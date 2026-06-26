## Description: <br>
Install 3x-ui panels on servers via SSH, create VLESS+Reality+TCP nodes with SOCKS5 outbound binding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[n0vemb](https://clawhub.ai/user/n0vemb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and server operators use this skill to automate 3x-ui panel installation, register panel access details, and create VLESS Reality nodes that route through SOCKS5 exits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make remote server changes, open node ports, alter Xray routing, and restart services. <br>
Mitigation: Use it only on servers you intend to modify, confirm target servers before execution, and review changes before relying on the new route. <br>
Risk: Panel, SSH, and SOCKS5 credentials may be stored or handled by local configuration and command execution. <br>
Mitigation: Keep servers.yaml out of version control, restrict file permissions, prefer SSH keys, and rotate exposed credentials. <br>
Risk: The implementation weakens SSH host-key and TLS certificate checks. <br>
Mitigation: Prefer verified SSH host keys and trusted TLS certificates; enable certificate verification or use a trusted CA where possible. <br>
Risk: The install workflow fetches and runs an upstream 3x-ui installer during execution. <br>
Mitigation: Inspect or pin the upstream installer before use and run it only in environments where that dependency is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/n0vemb/xui-node-manager) <br>
- [3x-ui upstream installer used by the skill](https://raw.githubusercontent.com/mhsanaei/3x-ui/master/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Markdown, Text, Files] <br>
**Output Format:** [Markdown and terminal output with shell commands, generated QR PNG files, and vless:// URIs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local server configuration files and generated QR-code image files.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
