## Description: <br>
Professional FortiGate security configuration generator based on CIS Benchmark standards for enterprise firewall hardening. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security teams, network architects, MSSPs, infrastructure-as-code practitioners, and compliance professionals use this skill to generate standardized FortiGate hardening configurations from selected security options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: External API requests may disclose sensitive firewall, identity, or architecture details. <br>
Mitigation: Use pseudonymous session IDs, omit userId when possible, and avoid sending secrets, firewall credentials, internal IP ranges, or confidential architecture details. <br>
Risk: Generated FortiGate configuration may not match the user's FortiOS version, current CIS guidance, or local change-control requirements. <br>
Mitigation: Review generated configuration against the target FortiOS version, current CIS guidance, and the organization's normal change-control process before deployment. <br>
Risk: Applying hardening changes without staging can disrupt administrative access, logging, authentication, or traffic flow. <br>
Mitigation: Test generated configuration in a controlled environment and apply changes through established firewall deployment and rollback procedures. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-fortigate-hardening) <br>
- [FortiGate hardening API docs](https://api.mkkpro.com:8135/docs) <br>
- [FortiGate hardening API endpoint](https://api.mkkpro.com/hardening/fortigate) <br>
- [ToolWeb](https://toolweb.in) <br>


## Skill Output: <br>
**Output Type(s):** [configuration, guidance] <br>
**Output Format:** [JSON API responses containing FortiGate configuration objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires hardeningOptions, sessionId, and timestamp; userId is optional. The skill generates configuration output and does not automatically change a firewall.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and OpenAPI info.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
