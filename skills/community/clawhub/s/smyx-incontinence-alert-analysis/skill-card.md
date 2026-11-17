## Description:

Analyzes caregiving images or videos for signs of wet clothing or abnormal excretion and provides caregivers with alerts, reports, and care suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Caregivers and care organizations use the skill to assess images or videos of older adults, bedridden patients, or infants for possible incontinence-related care needs and to review prior reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private caregiving images or videos and identity-linked information are sent to external services.

Mitigation: Obtain consent from the people monitored and approve cloud processing and report access before installation or use.

Risk: The skill may create or reuse a user identity and persist tokens locally.

Mitigation: Review identity and token retention practices, restrict access to stored credentials, and remove them when no longer needed.

Risk: A missed or incorrect alert could delay necessary care.

Mitigation: Have caregivers confirm alerts and continue routine human checks; do not rely on the skill as a substitute for professional care.

## Reference(s):

- [Incontinence alert API documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Caregiving analysis report or history table, with optional structured JSON and report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include alert levels, care suggestions, and a link to a cloud-hosted report.]

## Skill Version(s):

1.0.16 (source: ClawHub release metadata; bundled frontmatter says 1.0.20)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
