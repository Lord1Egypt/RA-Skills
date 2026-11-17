## Description:

Read-only UniFi network advisor covering the Site Manager cloud API and the Network Integration API for devices, clients, networks, firewall policy, VPN, DPI, ISP metrics, and related UniFi state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arseni-mik](https://clawhub.ai/user/arseni-mik)

### License/Terms of Use:

MIT-0

## Use Case:

Network operators, IT administrators, and support engineers use this skill to inspect UniFi environments, query read-only API state, and receive guidance about device health, clients, firewall policy, VPN status, ISP metrics, and related network configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive UniFi account, network inventory, client, firewall, VPN, voucher, IP address, and firmware information.

Mitigation: Install and run it only where read access to the UniFi cloud account and returned network details are acceptable, and treat outputs as confidential.

Risk: Site inventory metadata is cached locally for about 15 minutes without explicit permission hardening by the script.

Mitigation: Use the skill on trusted hosts and account profiles where local cache files are protected by the surrounding operating system permissions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/arseni-mik/skills/unifi-advisor)
- [OpenClaw](https://openclaw.ai)
- [UniFi Portal](https://unifi.ui.com)
- [UniFi API Host](https://api.ui.com)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown with inline shell commands and summarized JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include sensitive network inventory, client, firewall, VPN, IP address, voucher, firmware, and performance details from the user's UniFi account.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
