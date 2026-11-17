## Description:

Schema for tracking code review outcomes to enable feedback-driven skill improvement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to log code review outcomes, verdicts, rationales, and rule sources in a consistent CSV format for later review-quality analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feedback log entries may include repository file paths, line numbers, and issue rationales.

Mitigation: Review the chosen feedback-log destination and access controls before storing review outcomes.

Risk: Incorrect or weak rationales can reduce the usefulness of review-quality analysis.

Mitigation: Apply the skill's gates before appending a row, including evidence binding, attributable rule sources, artifact-backed verdicts, and valid CSV shape.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, text]

**Output Format:** [Markdown guidance with CSV schema, validation gates, taxonomy tables, and example feedback rows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defines a nine-field feedback log row for review findings and human verdicts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
