## Description:

Analyzes meal videos for eating habits and dietary patterns, producing structured reports and nutrition suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and wellness practitioners can submit meal videos to assess eating speed, habits, and dietary patterns and review reports with improvement suggestions. The reports are informational and do not replace professional medical or nutritional advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meal videos and related health-adjacent information are sent to a provider API.

Mitigation: Submit only media you are willing to share with the provider; avoid sensitive medical or private household footage unless its data practices are acceptable.

Risk: The skill silently creates or reuses a cloud-linked identity and retains authentication tokens locally for report history.

Mitigation: Review the identity, report retention, and local token practices before installing or using cloud history.

Risk: Automated dietary assessments can be mistaken for clinical advice.

Mitigation: Treat reports as informational and consult a qualified clinician or dietitian for medical or nutritional decisions.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/smyx-sunjinhui/skills/smyx-diet-analysis)
- [Diet analysis API documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Report links]

**Output Format:** [Text or JSON-formatted report with optional Markdown report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports basic, standard, and JSON detail levels and cloud report-history lookup.]

## Skill Version(s):

1.0.16 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
