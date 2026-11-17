## Description:

Bypass API rate limits by rotating VPN servers. Works with any OpenVPN-compatible VPN (ProtonVPN, NordVPN, Mullvad, etc.). Automatically rotates to new server every N requests for fresh IPs. Use for high-volume scraping, government APIs, geo-restricted data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acastellana](https://clawhub.ai/user/acastellana)

### License/Terms of Use:


## Use Case:

Developers and automation engineers use this skill to configure OpenVPN-based IP rotation around scraping or API collection workflows. Users should confirm that the target service and applicable law authorize their scraping, rate-limit, and geo-access behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed for rate-limit bypass and geo-access workflows that may violate service rules or law if used without authorization.

Mitigation: Confirm authorization from the relevant service and applicable legal requirements before using the skill.

Risk: The setup flow can make persistent passwordless sudo changes for OpenVPN and process-control commands.

Mitigation: Install only after review, preferably in an isolated environment, and remove or narrow sudoers entries when they are no longer required.

Risk: VPN credentials are stored in a plaintext local file.

Mitigation: Restrict file permissions, avoid shared machines, and use provider-specific credentials that can be rotated or revoked.

Risk: The disconnect logic can affect other OpenVPN sessions on the host.

Mitigation: Run on a dedicated machine or container and check for existing OpenVPN sessions before using connect, rotate, or disconnect commands.

## Reference(s):

- [ProtonVPN OpenVPN configuration download](https://protonvpn.com/support/vpn-config-download/)
- [NordVPN OpenVPN configuration files](https://nordvpn.com/ovpn/)
- [Mullvad OpenVPN configuration](https://mullvad.net/en/account/#/openvpn-config)
- [Skill release page](https://clawhub.ai/acastellana/skills/vpn-rotate-skill)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup guidance, CLI commands, Python decorator and class usage examples, and provider-specific configuration notes.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
