## Description: <br>
Professional network security assessment and gap analysis platform generating comprehensive audit reports across security domains and compliance frameworks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security teams, compliance officers, network administrators, MSSPs, and auditors use this skill to evaluate network security controls across 12 domains and produce scored findings, remediation guidance, and compliance mappings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends sensitive infrastructure and security-assessment details to an external service without clear privacy, retention, or access-control disclosure. <br>
Mitigation: Use only if you trust the service operator; confirm transmitted data, authentication requirements, report retention, and whether user IDs, session details, and infrastructure notes can be omitted or pseudonymized. <br>
Risk: Generated audit findings and compliance mappings may influence security or compliance decisions. <br>
Mitigation: Have qualified security staff review the report against source evidence and organizational requirements before using it for remediation planning or audit attestations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-network-security-audit) <br>
- [OpenAPI Specification](artifact/openapi.json) <br>
- [API Docs](https://api.mkkpro.com:8119/docs) <br>
- [Network Security Audit API Route](https://api.mkkpro.com/security/network-security-audit) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, JSON] <br>
**Output Format:** [JSON audit report with scores, findings, recommendations, and compliance mappings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires structured assessment data for all supported security domains; responses may include domain scores, critical findings, remediation recommendations, and framework mappings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and OpenAPI info) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
