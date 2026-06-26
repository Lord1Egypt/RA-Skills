## Description: <br>
Generates hardened pfSense firewall configurations based on specified security options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network administrators, security engineers, DevSecOps teams, and MSSPs use this skill to request hardened pfSense firewall configuration objects for review and change management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated pfSense changes could affect production access or firewall policy if applied without review. <br>
Mitigation: Review generated configurations through staging, change control, or peer review before applying them to pfSense. <br>
Risk: Requests may contain session IDs, user IDs, timestamps, hardening choices, or environment details that are sent to the API provider. <br>
Mitigation: Avoid sending secrets, real internal identifiers, detailed topology, or sensitive production data unless sharing it with the API provider is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-pfsense-hardening) <br>
- [OpenAPI specification](artifact/openapi.json) <br>
- [API documentation](https://api.mkkpro.com:8131/docs) <br>
- [API route](https://api.mkkpro.com/hardening/pfsense) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The API returns generated pfSense configuration objects and applied hardening rules for review before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and OpenAPI info.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
