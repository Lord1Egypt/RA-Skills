## Description:

Analyzes video of a pet in an airline carrier to estimate its respiratory rate and flag readings above 40 breaths per minute.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Pet owners and transport handlers can submit carrier video to estimate a pet’s resting breathing rate and review threshold alerts or prior reports. Results are for monitoring and do not provide a diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports credential and privacy concerns, actions beyond the stated video-analysis purpose, and a mismatch involving export-only behavior.

Mitigation: Avoid installation until credential handling, URL destinations, export behavior, and user-data and history capabilities are clarified.

Risk: The security evidence is incomplete because a referenced local path was missing.

Mitigation: Resolve the missing path and review the complete evidence before relying on scanner results.

## Reference(s):

- [API documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured respiratory-rate reports and Markdown history tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Breaths per minute, threshold alerts, monitoring guidance, and report links; no disease diagnosis.]

## Skill Version(s):

1.0.12 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
