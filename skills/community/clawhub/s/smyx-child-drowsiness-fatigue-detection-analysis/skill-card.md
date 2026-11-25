## Description:

Analyzes a child’s facial video for visual signs associated with drowsiness, including eye closure and head movements, and returns a fatigue assessment and report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Parents, teachers, or developers can use the skill to request a visual drowsiness assessment of a child’s study video and review fatigue indicators, a score, and rest reminders. The skill documentation says its results are for learning support and are not medical diagnoses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marked the skill suspicious because of reported broad account, credential, and data handling behavior and a mismatch with its stated fatigue-analysis purpose; the scan was partial and could not verify some delegated behavior.

Mitigation: Avoid installation until the publisher clarifies account creation, credential storage, remote destinations, and video upload behavior, and the missing or unverified behavior has been reviewed.

Risk: The workflow concerns video of children and may send video for remote analysis.

Mitigation: Before use, obtain guardian consent and confirm where video and reports are sent, stored, and protected; do not submit sensitive footage until those details are clear.

## Reference(s):

- [API interface and reported fatigue fields](artifact/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis results, JSON, Markdown, Guidance]

**Output Format:** [Structured JSON analysis report; Markdown history report list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include fatigue metrics, a score and level, detected events, a summary, rest prompts, and report links.]

## Skill Version(s):

1.0.16 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
