## Description: <br>
Unifly helps agents manage Ubiquiti UniFi network infrastructure through the unifly CLI, including devices, clients, networks, WiFi, firewall, NAT, VPN, DNS, monitoring, backups, and raw API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hyperb1iss](https://clawhub.ai/user/hyperb1iss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, network administrators, and operations engineers use this skill to plan and execute UniFi controller tasks through the unifly CLI. It supports inventory, configuration changes, event monitoring, incident response, backups, and automation across UniFi sites and controllers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents through broad control of live UniFi infrastructure, including network, firewall, NAT, VPN, admin, backup, reboot, poweroff, and raw API operations. <br>
Mitigation: Use a least-privilege UniFi account and require explicit human approval before mutating admin, VPN, raw API, delete, reboot, poweroff, or bulk operations. <br>
Risk: Automation examples and raw API passthrough can change production network access or expose under-scoped controller functionality. <br>
Mitigation: Review proposed commands and payload files before execution, separate read-only workflows from write workflows, and prefer read-before-write checks with structured JSON output. <br>
Risk: Event data, controller details, API keys, and hotspot voucher codes may be sensitive if copied to external or plaintext locations. <br>
Mitigation: Keep credentials in environment variables or the OS keyring, sanitize exported event or voucher data, and avoid sending sensitive outputs to external services without review. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hyperb1iss/skills/unifly) <br>
- [unifly Command Reference](references/commands.md) <br>
- [UniFi Networking Concepts](references/concepts.md) <br>
- [Automation Workflows](references/workflows.md) <br>
- [Configuration Example](examples/config.toml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, JSON payloads, and configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Often favors JSON CLI output for agent parsing and may produce file-based payload templates for create/update workflows.] <br>

## Skill Version(s): <br>
0.8.3 (source: server release metadata; artifact frontmatter and release changelog mention 0.9.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
