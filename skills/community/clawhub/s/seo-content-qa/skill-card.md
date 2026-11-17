## Description:

Score an SEO draft before it ships against its brief, checking intent, structure, human voice, product facts, competitor claims, links, images, schema and publishing readiness, with a PASS/FAIL verdict out of 40.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romeoseo](https://clawhub.ai/user/romeoseo)

### License/Terms of Use:

MIT-0

## Use Case:

External SEO writers, editors, and content teams use the skill to check drafts against a brief before approval or publication. It returns a pass/fail verdict, score, required fixes, and residual risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Draft structured data may be sent to third-party validators, which could disclose unpublished or sensitive content.

Mitigation: Prefer local validation; before using an external validator, review the data and redact sensitive details.

Risk: The security scan is incomplete because a referenced local path was missing, so it may not cover all relevant material.

Mitigation: Review the installed skill and its referenced files before relying on the scan as a complete assessment.

## Reference(s):

- [SEO Content QA skill page](https://romeoseo.com/skills/seo-content-qa)
- [ClawHub release page](https://clawhub.ai/romeoseo/skills/seo-content-qa)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Text, Markdown]

**Output Format:** [Markdown report with a PASS/FAIL verdict, score, findings, and recommended fixes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A score out of 40, critical-fail status, required fixes, optional improvements, and residual risks]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
