## Description:

Enterprise-grade Sarbanes-Oxley assessment platform that evaluates organizational compliance with SOX requirements across multiple control domains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Compliance, audit, IT security, and managed service provider teams use this skill to submit SOX control status data and receive structured compliance scores, findings, and remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SOX assessment requests may include sensitive compliance details sent to an external API.

Mitigation: Use only organization-approved data sharing and avoid raw audit evidence, secrets, customer or employee data, financial details, and confidential control weaknesses in request notes.

Risk: The evidence does not provide enough disclosure about provider data handling for real compliance environments.

Mitigation: Confirm retention, access, deletion, residency, and contractual controls with the provider before sending SOX assessment content.

## Reference(s):

- [OpenAPI schema](artifact/openapi.json)
- [SOX Compliance API documentation](https://api.mkkpro.com:8039/docs)
- [SOX Compliance API route](https://api.mkkpro.com/compliance/sox-compliance)
- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/sox-compliance)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON assessment results with text remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces compliance percentages, section findings, and prioritized remediation actions from submitted control data.]

## Skill Version(s):

1.0.0 (source: server release metadata and OpenAPI info.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
