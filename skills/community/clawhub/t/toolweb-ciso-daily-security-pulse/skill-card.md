## Description:

Comprehensive daily security posture assessment tool that provides CISOs with actionable security insights and metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Security executives, security operations teams, and integration developers use this skill to submit security posture metrics and receive daily security scores, risk levels, prioritized recommendations, and maturity indicators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Aggregated security posture metrics and user or session identifiers may be sent to ToolWeb.in.

Mitigation: Avoid submitting secrets, hostnames, asset identifiers, incident details, customer data, or personally identifying user IDs unless the organization has approved that data sharing and retention arrangement.

Risk: The external service's data handling and retention scope is not fully disclosed in the provided evidence.

Mitigation: Confirm vendor data-handling, retention, and access controls before using the skill with sensitive organizational security data.

## Reference(s):

- [CISO Daily Security Pulse API Docs](https://api.toolweb.in:8203/docs)
- [CISO Daily Security Pulse API Route](https://api.toolweb.in/tools/ciso-daily-security-pulse)
- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/toolweb-ciso-daily-security-pulse)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON response with security score, risk level, recommendations, metrics, and assessment timestamps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Assessment input requires security posture data; session ID, user ID, and timestamp are optional.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
