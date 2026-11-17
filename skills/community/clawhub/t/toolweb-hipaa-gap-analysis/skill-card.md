## Description:

Assesses HIPAA compliance across administrative, physical, technical, privacy, and breach notification rule areas and produces a gap report with scoring, deficiencies, and remediation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Compliance practitioners at covered entities, business associates, and related healthcare organizations use this skill to evaluate HIPAA control coverage, identify gaps, and prioritize remediation before audit or compliance review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends sensitive compliance and PHI-handling details to a third-party API without enough privacy or handling disclosure.

Mitigation: Before use with regulated health data, confirm the provider's privacy, retention, logging, encryption, jurisdiction, and BAA terms, and avoid submitting patient identifiers or unnecessary PHI.

Risk: The HIPAA assessment output may be incomplete or unsuitable as the sole basis for compliance decisions.

Mitigation: Treat the report as advisory and have qualified legal, compliance, or security reviewers validate findings before audit preparation or remediation commitments.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/toolweb-hipaa-gap-analysis)
- [ToolWeb HIPAA gap analysis API](https://portal.toolweb.in/apis/compliance/hipaa-gap-analysis)
- [ToolWeb](https://toolweb.in)
- [ToolWeb MCP server](https://hub.toolweb.in)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON report with compliance scores, rule-by-rule gaps, deficiencies, remediation actions, regulatory exposure, and audit readiness rating]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires organization profile, PHI handling details, and HIPAA control-status inputs; output is advisory and should be reviewed by qualified compliance or legal staff.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
