## Description: <br>
Query and monitor a UniFi network using a UniFi Integration API key and compatible read-only UniFi Network endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrjq1987](https://clawhub.ai/user/mrjq1987) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network administrators and technical operators use this skill to inspect read-only UniFi site, device, client, health, alarm, DPI, network, and WLAN status from a UniFi OS console or Cloud Gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose detailed UniFi network, device, client, alarm, and traffic metadata. <br>
Mitigation: Install only where read access to this data is acceptable, avoid sharing raw endpoint dumps, and review outputs before relaying them. <br>
Risk: Credential handling can be overly broad if local admin credentials or permissive credential files are used. <br>
Mitigation: Use a scoped UniFi Integration API key, store it in the configured credentials file with restrictive permissions, and rotate it if exposed. <br>
Risk: The helper scripts use disabled TLS certificate verification for local UniFi endpoints. <br>
Mitigation: Prefer fixing local certificate trust and avoid relying on disabled TLS verification except where explicitly accepted for the environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mrjq1987/unifi-inforjota-integration) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/mrjq1987) <br>
- [UniFi read-only endpoint reference](artifact/references/unifi-readonly-endpoints.md) <br>
- [Community UniFi Controller API reference](https://ubntwiki.com/products/software/unifi-controller/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands plus human-readable tables or JSON from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only UniFi monitoring outputs may include sensitive network, device, client, alarm, and traffic metadata.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
