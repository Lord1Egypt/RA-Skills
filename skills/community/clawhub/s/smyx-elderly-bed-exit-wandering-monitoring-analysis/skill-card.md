## Description:

Analyzes nighttime monitoring footage for elderly bed exits, prolonged wandering, and extended immobility, and returns a structured report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Caregivers and residential care teams use the skill to review nighttime footage for possible bed exits, wandering, and extended immobility, and to retrieve prior monitoring reports. Results are for care reference and require human confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security assessment reports credential and data-handling concerns, behavior beyond the stated monitoring purpose, and gaps in the promised analysis behavior.

Mitigation: Review before installation and verify video processing, credential handling, and runtime permissions before use.

Risk: The security scan was partial because a referenced path was missing, so some monitoring behavior could not be verified.

Mitigation: Confirm the skill's behavior and have a caregiver verify alerts; the skill describes its results as care guidance rather than a replacement for human checks.

## Reference(s):

- [API documentation](references/api_doc.md)
- [Analysis API documentation](skills/smyx_analysis/references/api_doc.md)
- [Skill demo](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [JSON, Markdown]

**Output Format:** [Structured analysis reports and report lists, with report export links when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analysis reports may include a report export link; history queries return report records.]

## Skill Version(s):

1.0.24 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
