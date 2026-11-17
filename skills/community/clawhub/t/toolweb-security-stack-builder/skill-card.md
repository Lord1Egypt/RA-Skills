## Description:

Comprehensive cybersecurity technology stack recommendation platform that generates personalized security tool recommendations based on organizational assessment data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Security architects, CISO offices, enterprise security teams, compliance officers, cloud architects, and IT teams use this skill to request security tool-stack recommendations from organizational assessment data, compliance needs, budget, maturity, deployment model, and priorities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Organization security context, compliance needs, session identifiers, timestamps, and optional user IDs are sent to the provider's hosted API.

Mitigation: Confirm vendor and privacy approval before use, send only the minimum organizational context needed, and avoid secrets, sensitive internal architecture details, and regulated personal data unless approved.

Risk: Generated security-stack recommendations and cost estimates may be incomplete or unsuitable for a specific environment.

Mitigation: Have qualified security, compliance, and procurement reviewers validate recommendations before acquisition or implementation.

## Reference(s):

- [Security Stack Builder API Docs](https://api.mkkpro.com:8122/docs)
- [Security Stack Builder API Route](https://api.mkkpro.com/security/security-stack-builder)
- [ToolWeb](https://toolweb.in)
- [ToolWeb OpenClaw](https://toolweb.in/openclaw/)
- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/toolweb-security-stack-builder)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON API response with security tool recommendations, compliance mapping, estimated annual costs, and implementation phases.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendation requests include organization profile, compliance, priorities, session identifiers, timestamps, and optional user IDs.]

## Skill Version(s):

1.0.0 (source: release metadata and OpenAPI info.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
