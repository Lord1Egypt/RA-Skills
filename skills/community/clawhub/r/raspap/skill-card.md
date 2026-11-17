## Description:

Query and troubleshoot a RaspAP access point via its local REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[naamah75](https://clawhub.ai/user/naamah75)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and network administrators use this skill to inspect RaspAP access point status, clients, DHCP, DNS, firewall, VPN, and networking diagnostics through the local REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: RaspAP API keys and raw configuration data can expose network secrets.

Mitigation: Keep the API key in an environment variable or key file, avoid printing it, rely on redacted output by default, and use raw output only when explicitly needed.

Risk: Restart, reload, or configuration actions can interrupt Wi-Fi, DHCP, DNS, routing, firewall, OpenVPN, or WireGuard service.

Mitigation: Default to read-only checks and require explicit approval before any action that could affect network services.

Risk: Raw configuration endpoints may reveal passphrases, certificates, private keys, credentials, or auth file names.

Mitigation: Avoid raw configuration endpoints unless necessary; when inspection is unavoidable, summarize only non-secret fields.

Risk: The referenced raspap-api helper is not included in this artifact.

Mitigation: Confirm the helper exists locally and comes from a trusted source before relying on it.

## Reference(s):

- [ClawHub RaspAP skill page](https://clawhub.ai/naamah75/skills/raspap)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON endpoint summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to read-only diagnostics and redacted sensitive JSON fields; raw configuration output requires explicit need.]

## Skill Version(s):

0.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
