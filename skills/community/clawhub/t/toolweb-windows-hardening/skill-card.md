## Description: <br>
Professional Windows Security Configuration Generator for automated hardening policy creation and deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security teams, system administrators, compliance professionals, and developers use this skill to generate Windows security hardening configurations tailored to organizational policy requirements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a third-party ToolWeb/api.mkkpro API provider. <br>
Mitigation: Verify that the provider is trusted before installing or using the skill. <br>
Risk: Session or user identifiers could expose personal or production-sensitive values. <br>
Mitigation: Avoid putting sensitive values in sessionId or userId. <br>
Risk: Generated Windows policies may affect real systems if applied without validation. <br>
Mitigation: Review generated policies in a test environment and keep a rollback plan before applying them to production systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-windows-hardening) <br>
- [Publisher profile](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>
- [API docs](https://api.mkkpro.com:8125/docs) <br>
- [Kong route](https://api.mkkpro.com/hardening/windows) <br>
- [OpenAPI specification](artifact/openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, configuration, guidance] <br>
**Output Format:** [JSON API responses with generated hardening profile metadata and download URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated Windows policies should be reviewed in a test environment before production use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and OpenAPI info.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
