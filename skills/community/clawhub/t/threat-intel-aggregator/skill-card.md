## Description:

Aggregates and analyzes threat intelligence data to check targets against known threats and security risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Security teams, incident responders, compliance professionals, and developers use this skill to submit IPs, domains, file hashes, or URLs for consolidated threat checks and remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted IPs, domains, URLs, or file hashes are shared with the external API provider.

Mitigation: Avoid submitting sensitive internal indicators unless external sharing is acceptable for the organization.

## Reference(s):

- [Threat Intel Aggregator on ClawHub](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/threat-intel-aggregator)
- [API Docs](https://api.mkkpro.com:8009/docs)
- [Kong Route](https://api.mkkpro.com/security/threat-intel-aggregator)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON threat assessment with human-readable recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a target assessment, threat status, findings, confidence scores, risk score, recommendations, and aggregation timestamp.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
