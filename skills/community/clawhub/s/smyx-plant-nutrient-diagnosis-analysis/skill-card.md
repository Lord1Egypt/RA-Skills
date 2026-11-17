## Description:

Helps analyze plant-leaf images and videos for possible nutrient deficiencies, returning a structured report with a confidence score and general guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Home gardeners, greenhouse growers, and plant-care assistants use the skill to review leaf images or videos for possible nutrient deficiencies and receive a likely nutrient, confidence level, and general next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this release suspicious with high confidence, citing mismatches with the plant-diagnosis description and undeclared data handling.

Mitigation: Review the security findings and wait for the maintainer to clarify the behavior before installing.

Risk: The security guidance flags uncertainty about video processing, external media handling, account registration, and local credential storage; the scan was partial and does not establish that all behavior was reviewed.

Mitigation: Ask the maintainer to explain these data and credential flows and complete review of the referenced behavior before sending images or videos.

Risk: The security summary says actions may run despite an export-only option.

Mitigation: Do not rely on export-only mode to prevent analysis; use the skill only after this behavior is fixed or explained.

## Reference(s):

- [API reference](artifact/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-plant-nutrient-diagnosis-analysis)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Structured diagnosis report in text, Markdown, or JSON, with report links when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include likely nutrient deficiency, confidence score, and general guidance. Results are advisory; symptoms can overlap, and fertilizer dosage is not provided.]

## Skill Version(s):

1.0.16 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
