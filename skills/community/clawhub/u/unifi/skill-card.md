## Description: <br>
Query and monitor UniFi network via local gateway API (Cloud Gateway Max / UniFi OS). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jmagar](https://clawhub.ai/user/jmagar) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, network administrators, and operators use this skill to inspect UniFi device status, active clients, health, traffic, and alerts from a local UniFi OS gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: UniFi monitoring output can include sensitive client, firewall, VLAN, routing, and inventory data that may be written to local files. <br>
Mitigation: Use a dedicated least-privilege UniFi account, restrict credential file permissions, and inspect, relocate, or disable dashboard/debug output files before running in sensitive environments. <br>


## Reference(s): <br>
- [UniFi Local Gateway Read-Only Endpoints](references/unifi-readonly-endpoints.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jmagar/unifi) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with bash commands, human-readable tables, optional JSON output, and a generated local Markdown inventory file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq plus UniFi gateway credentials; dashboard output may persist network inventory locally.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
