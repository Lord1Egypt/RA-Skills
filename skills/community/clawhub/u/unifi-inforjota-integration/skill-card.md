## Description:

Query and monitor a UniFi network using a UniFi Integration API key plus compatible read-only UniFi Network endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrjq1987](https://clawhub.ai/user/mrjq1987)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and network operators use this skill to inspect UniFi sites, devices, clients, health, alarms, WLANs, networks, and DPI availability from a Cloud Gateway or UniFi OS console.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential handling can expose UniFi access tokens or administrator credentials if configuration files are created or stored insecurely.

Mitigation: Use a dedicated read-only UniFi API key and restrict the credential file to owner-only permissions.

Risk: The skill's scripts skip TLS certificate verification, which can expose requests to interception on untrusted networks.

Mitigation: Avoid use until TLS verification is fixed or configure a trusted gateway certificate or certificate authority.

Risk: Monitoring output can reveal sensitive network names, IP addresses, MAC addresses, topology, alarms, and traffic metadata.

Mitigation: Treat command output as sensitive and avoid sharing raw payloads unless necessary.

## Reference(s):

- [UniFi Local Gateway Read-Only API Calls](references/unifi-readonly-endpoints.md)
- [Community UniFi Controller API reference](https://ubntwiki.com/products/software/unifi-controller/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include sensitive network inventory, device identifiers, IP addresses, MAC addresses, topology, alarms, and traffic metadata.]

## Skill Version(s):

1.0.3 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
