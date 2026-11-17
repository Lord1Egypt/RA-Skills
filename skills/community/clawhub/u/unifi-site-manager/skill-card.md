## Description:

Monitor and configure UniFi network infrastructure, with automatic routing between a local gateway and the cloud connector for hosts, sites, devices, clients, WLANs, radios, firmware, and events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[odrobnik](https://clawhub.ai/user/odrobnik)

### License/Terms of Use:


## Use Case:

Developers, operators, and network administrators use this skill to inspect UniFi infrastructure and make configuration changes for clients, WLANs, radio settings, DNS, firmware status, and events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live UniFi configuration commands can immediately affect WLAN, DNS, radio, and client settings.

Mitigation: Use least-privilege API keys, review proposed commands before execution, and apply changes first in a non-critical site or maintenance window.

Risk: Local gateway access depends on trusting the expected TLS certificate.

Mitigation: Configure and maintain the local gateway certificate fingerprint before using local HTTPS access.

Risk: Running the skill against a production network can affect connectivity without built-in rollback safeguards.

Mitigation: Install dependencies in an isolated environment and keep a separate rollback plan for any network settings changed by set-wlan, set-network-dns, set-radio, set-client, or label-client.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/odrobnik/skills/unifi-site-manager)
- [Setup instructions](artifact/SETUP.md)
- [UniFi Site Manager](https://unifi.ui.com)
- [UniFi API base URL](https://api.ui.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell command examples; CLI commands can return human-readable text or raw JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a UniFi API key; optional local gateway settings enable direct local access when configured.]

## Skill Version(s):

3.2.1 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
