## Description: <br>
Query and troubleshoot a RaspAP access point via its local REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[naamah75](https://clawhub.ai/user/naamah75) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network administrators and technical operators use this skill to inspect RaspAP access point status, clients, DHCP, DNS, firewall, VPN, and related diagnostics through the local REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses RaspAP API credentials and may expose API keys or raw configuration secrets if handled carelessly. <br>
Mitigation: Keep the API key private, prefer RASPAP_API_KEY or RASPAP_KEY_FILE, rely on default redaction, and summarize only non-secret configuration fields before sharing output. <br>
Risk: Restart, reload, or configuration changes can interrupt Wi-Fi, DHCP, DNS, routing, firewall, OpenVPN, or WireGuard service. <br>
Mitigation: Default to read-only checks and ask for explicit approval before any disruptive action or network service change. <br>
Risk: Querying an unintended device can expose local network information or affect systems the user does not administer. <br>
Mitigation: Use this only for RaspAP devices the user administers and verify RASPAP_HOST before making API requests. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [API output is redacted by default; raw configuration output should be used only when explicitly needed.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
