## Description: <br>
Query and monitor a UniFi network through the local UniFi OS gateway API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ricanwarfare](https://clawhub.ai/user/ricanwarfare) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network administrators, homelab operators, and agents assisting them use this skill to check UniFi device status, active clients, site health, top applications, and recent alerts from a local gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores UniFi gateway credentials on disk. <br>
Mitigation: Use a dedicated least-privilege local UniFi account and protect ~/.openclaw/credentials/unifi.json with restrictive file permissions. <br>
Risk: Dashboard execution can save raw private network data locally in dashboard_debug_dump.json. <br>
Mitigation: Remove or disable debug dump behavior unless raw local network data should intentionally be persisted, and delete generated dumps when they are no longer needed. <br>
Risk: The skill accesses private network infrastructure from the machine where it runs. <br>
Mitigation: Run it only on trusted machines and trusted networks with an expected UniFi gateway target. <br>


## Reference(s): <br>
- [UniFi Read-Only Endpoints](references/unifi-readonly-endpoints.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ricanwarfare/unifi-network) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or plain text with shell commands, tables, and optional JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; reads from a local UniFi gateway and may return private network inventory, traffic, health, and alert data.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
