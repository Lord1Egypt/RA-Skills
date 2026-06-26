## Description: <br>
Professional VMware ESXi 8.0 security configuration generator that produces hardened configuration files based on industry best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Infrastructure security teams, VMware administrators, compliance teams, and managed service providers use this skill to generate VMware ESXi 8.0 hardening configurations from selected firewall, authentication, logging, and service controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests are sent to an external API provider with selected hardening options, a timestamp, and a session identifier. <br>
Mitigation: Use a pseudonymous sessionId, omit userId unless needed, and avoid sending unnecessary identifying data. <br>
Risk: Generated ESXi hardening files may need validation before use in a specific production environment. <br>
Mitigation: Review and test generated files in a non-production environment before applying them to production hosts. <br>


## Reference(s): <br>
- [API documentation](https://api.mkkpro.com:8146/docs) <br>
- [VMware ESXi hardening API route](https://api.mkkpro.com/hardening/vmware-esxi) <br>


## Skill Output: <br>
**Output Type(s):** [configuration, JSON, guidance] <br>
**Output Format:** [JSON response with hardening profile details, summary text, and encoded configuration files such as YAML, firewall rules, and audit policy files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires selected hardening options, sessionId, and timestamp; userId is optional.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and OpenAPI info.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
