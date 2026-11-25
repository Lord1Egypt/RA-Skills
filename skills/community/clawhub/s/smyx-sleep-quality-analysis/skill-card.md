## Description:

Analyzes sleep-monitoring videos to identify sleep stages, movement, nighttime awakenings, and possible sleep apnea, and produces a structured report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

People reviewing sleep-monitoring recordings can use the skill to summarize sleep stages, movement, awakenings, and possible breathing events. The report is for reference and does not replace professional sleep monitoring or a clinician’s diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security guidance flags external processing of sensitive sleep footage without a clear consent step.

Mitigation: Obtain explicit consent before submitting footage, and avoid uploading recordings of anyone who has not agreed.

Risk: The security guidance flags credential forwarding, silent account registration, and token storage.

Mitigation: Review account and credential handling before installation, and do not provide credentials unless you understand how they are used and stored.

Risk: The security scan was partial and does not establish that every referenced component was assessed.

Mitigation: Review unresolved components before relying on the scan’s coverage.

## Reference(s):

- [API documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured sleep-analysis report in JSON or Markdown, with findings and report links where available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sleep-stage, movement, awakening, and possible apnea findings; results are informational.]

## Skill Version(s):

1.0.22 (source: server-resolved release metadata; artifact frontmatter says 1.0.24)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
