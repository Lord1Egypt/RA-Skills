## Description:

Evaluates Zero Trust maturity across 6 principles for both Conventional (Infrastructure) and AI Era (Data & Model) dimensions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Security architects, CISOs, AI/ML leaders, and enterprise security teams use this skill to submit Zero Trust assessment data and receive maturity scores, principle-level findings, and remediation recommendations for infrastructure and AI environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Assessment submissions may contain sensitive security posture, architecture, or user identifier data and are sent to ToolWeb's external API.

Mitigation: Redact sensitive architecture details and unnecessary user identifiers, and review ToolWeb privacy, retention, and contractual terms before using real enterprise security data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/toolweb-zero-trust-for-ai-maturity-assessment)
- [ToolWeb API route](https://api.toolweb.in/security/zertruforaimatass)
- [ToolWeb API docs](https://api.toolweb.in:8161/docs)
- [OpenAPI specification](artifact/openapi.json)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON responses with maturity scores, principle-level breakdowns, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires submitting assessment data to ToolWeb's external API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
