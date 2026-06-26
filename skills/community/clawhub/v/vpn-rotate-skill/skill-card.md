## Description: <br>
Rotates OpenVPN-compatible VPN servers so agents can run scraping or data-collection workflows with periodic IP changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[acastellana](https://clawhub.ai/user/acastellana) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to configure and invoke OpenVPN server rotation for authorized scraping, geo-restricted data access, and API workflows that need controlled IP changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup grants persistent passwordless sudo for OpenVPN and process-kill commands. <br>
Mitigation: Install only on a trusted machine, restrict sudoers entries to the required commands, and remove the sudoers entry when the skill is no longer needed. <br>
Risk: VPN credentials may be stored on disk in a plaintext credentials file. <br>
Mitigation: Protect the credentials file with restrictive permissions, use a dedicated VPN account where possible, and avoid storing shared or high-value credentials. <br>
Risk: VPN rotation and disconnect operations can disrupt other OpenVPN sessions on the host. <br>
Mitigation: Run the skill on a dedicated host or isolated environment and avoid sharing that host with unrelated OpenVPN workloads. <br>
Risk: The skill is designed for rate-limit bypass and IP rotation workflows. <br>
Mitigation: Use it only for authorized traffic and confirm that the target service terms and applicable laws permit the intended collection activity. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/acastellana/vpn-rotate-skill) <br>
- [ProtonVPN OpenVPN configuration guide](https://protonvpn.com/support/vpn-config-download/) <br>
- [NordVPN OpenVPN configuration files](https://nordvpn.com/ovpn/) <br>
- [Mullvad OpenVPN configuration generator](https://mullvad.net/en/account/#/openvpn-config) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local OpenVPN configuration, VPN credentials, and host sudo permissions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
