## Description: <br>
Monitor and configure UniFi network infrastructure. Auto-routes between local gateway and cloud connector. Manage hosts, sites, devices, clients, WLANs, radios, firmware, and events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[odrobnik](https://clawhub.ai/user/odrobnik) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Network administrators, developers, and agents use this skill to inspect UniFi sites and devices, review clients and events, and propose or run supported configuration changes for WLAN, DNS, radio, firmware, and client labeling workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses sensitive UniFi API keys to access cloud and local gateway APIs. <br>
Mitigation: Use dedicated, revocable API keys with the least privileges available, and prefer protected environment variables or tightly protected config.json storage. <br>
Risk: Supported set-* commands can change live network settings and disrupt connectivity. <br>
Mitigation: Manually review every proposed configuration command before running it, especially WLAN, DNS, radio, firmware, and client-labeling changes. <br>
Risk: Local gateway access depends on HTTPS certificate handling. <br>
Mitigation: Configure gateway_fingerprint for local access and update it after gateway certificate changes such as firmware updates or resets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/odrobnik/unifi-site-manager) <br>
- [Skill homepage](https://github.com/odrobnik/unifi-skill) <br>
- [Setup guide](SETUP.md) <br>
- [UniFi Site Manager](https://unifi.ui.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands, configuration snippets, and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires UniFi API credentials and can route between cloud and local gateway access depending on configuration.] <br>

## Skill Version(s): <br>
3.2.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
