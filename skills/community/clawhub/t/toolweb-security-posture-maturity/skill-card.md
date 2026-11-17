## Description:

Professional multi-dimensional security maturity evaluation platform that assesses organizational security across eight critical domains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Security teams, compliance officers, enterprise architects, and agents use this skill to submit maturity scores across eight security domains and receive an overall maturity level, domain-level results, and improvement recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Assessment scores, session identifiers, optional user identifiers, and timestamps may be sent to a third-party service.

Mitigation: Use pseudonymous session IDs, omit userId when possible, and avoid submitting organization names or sensitive internal details unless approved by policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/toolweb-security-posture-maturity)
- [Security Posture Maturity API route](https://api.mkkpro.com/security/security-posture-maturity)
- [Security Posture Maturity API docs](https://api.mkkpro.com:8121/docs)
- [ToolWeb](https://toolweb.in)

## Skill Output:

**Output Type(s):** [API Calls, JSON, guidance]

**Output Format:** [JSON responses with assessment scores, maturity levels, domain status, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Assessment requests include eight required integer domain scores from 1 to 5, a required session identifier, a required timestamp, and an optional user identifier.]

## Skill Version(s):

1.0.0 (source: server release metadata and OpenAPI info.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
