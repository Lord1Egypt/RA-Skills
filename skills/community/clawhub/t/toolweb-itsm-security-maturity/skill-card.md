## Description:

Comprehensive ITSM/ITIL security maturity evaluation platform for assessing organizational compliance and process maturity across eight critical ITSM domains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Security architects, ITSM service managers, compliance officers, and enterprise security teams use this skill to submit ITSM process maturity scores and receive maturity levels plus prioritized improvement recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Assessment submissions are sent to a third-party API and can include ITSM maturity scores, session IDs, timestamps, and optional user IDs.

Mitigation: Use pseudonymous session and user identifiers where possible and avoid submitting sensitive organizational details beyond the required 0-5 assessment scores.

Risk: Maturity scores and recommendations may be used to support compliance or process-improvement decisions.

Mitigation: Review outputs with security, ITSM, and compliance owners before relying on them for audit, control, or resource-allocation decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/toolweb-itsm-security-maturity)
- [Provider API documentation](https://api.mkkpro.com:8104/docs)
- [Provider API route](https://api.mkkpro.com/compliance/itsm-maturity)
- [OpenAPI specification](artifact/openapi.json)

## Skill Output:

**Output Type(s):** [JSON, guidance]

**Output Format:** [JSON API responses with maturity scores, maturity levels, status, and recommendation text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Assessment requests include ITSM maturity scores, session IDs, timestamps, and optional user IDs.]

## Skill Version(s):

1.0.0 (source: server release metadata and OpenAPI info.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
