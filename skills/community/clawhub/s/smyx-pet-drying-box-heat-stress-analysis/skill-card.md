## Description:

Analyzes pet drying box videos for panting, tongue color, and movement signals associated with heat stress, then reports a risk level and safety guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Pet drying box operators, groomers, and veterinary teams use video analysis to review visible heat stress signals and receive a risk level with safety guidance. The result is an observational aid, not a veterinary diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Videos and URLs may be uploaded to Life Emergence services, including when an export-only setting is expected.

Mitigation: Use only footage authorized for upload, verify the effective export and API destination controls, and confirm the services’ retention and access policies before processing private footage.

Risk: Accounts may be reused across users and credentials may be retained.

Mitigation: Use separate accounts for separate users, protect credentials, and prefer a corrected release before using private footage or sharing the installation.

Risk: Server-side analysis accuracy is unverified, so a risk assessment may be incomplete.

Mitigation: Treat results as an observational warning rather than a diagnosis; monitor the animal directly and stop drying, lower the temperature, and ventilate for high or urgent warnings.

## Reference(s):

- [API reference](references/api_doc.md)
- [Pet heat stress analysis API details](skills/smyx_analysis/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown]

**Output Format:** [Structured analysis results with observations, a risk level, safety guidance, and report links when available; Markdown tables for history listings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video observations and recommendations; does not provide diagnosis or treatment advice.]

## Skill Version(s):

1.0.14 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
