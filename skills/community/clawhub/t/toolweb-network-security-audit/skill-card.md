## Description:

Professional network security assessment and gap analysis platform generating comprehensive audit reports across security domains and compliance frameworks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Security teams, compliance officers, MSSPs, and network administrators use this skill to submit checkpoint-based network security assessments and receive audit scores, findings, remediation recommendations, and compliance mapping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit notes may contain internal hostnames, IP addresses, vulnerabilities, credentials, firewall rules, or compliance findings.

Mitigation: Use sanitized assessment data unless the organization trusts the external API operator and has approval to transmit security assessment details.

Risk: Security evidence says the skill sends sensitive security posture details to an external API without enough disclosure about data handling or user control.

Mitigation: Review the API operator, data handling expectations, and organizational approval requirements before installing or using the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/toolweb-network-security-audit)
- [API Docs](https://api.mkkpro.com:8119/docs)
- [Kong Route](https://api.mkkpro.com/security/network-security-audit)
- [OpenAPI Specification](artifact/openapi.json)
- [ToolWeb](https://toolweb.in)

## Skill Output:

**Output Type(s):** [json, text, guidance]

**Output Format:** [JSON audit reports with narrative summaries, findings, recommendations, scores, and compliance mappings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes assessment data across 12 network security domains.]

## Skill Version(s):

1.0.0 (source: release evidence and OpenAPI info.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
