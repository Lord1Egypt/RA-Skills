## Description: <br>
Professional security configuration generator for Cisco Firepower Threat Defense based on CIS Benchmark v1.0.0. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security teams and network administrators use this skill to request standards-aligned Cisco Firepower Threat Defense hardening configurations. It helps generate draft CLI commands and policy XML for review before firewall changes are applied. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated firewall configurations could affect sensitive network operations if applied without review. <br>
Mitigation: Treat generated configurations as drafts, test them in a non-production environment, and keep backups, rollback steps, and out-of-band management access ready. <br>
Risk: Requests to the external API may disclose sensitive topology or organization identifiers. <br>
Mitigation: Avoid sending sensitive infrastructure details unless the external API operator is trusted, and minimize session or user identifiers where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-cisco-ftd-hardening) <br>
- [Cisco FTD hardening API route](https://api.mkkpro.com/hardening/cisco-ftd) <br>
- [Cisco FTD hardening API docs](https://api.mkkpro.com:8141/docs) <br>
- [ToolWeb](https://toolweb.in) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON responses containing hardening status, generated CLI commands, and policy XML.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requests include hardeningOptions, sessionId, and timestamp, with optional userId for attribution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and OpenAPI info.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
