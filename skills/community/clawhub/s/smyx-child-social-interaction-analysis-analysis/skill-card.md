## Description:

Using fixed cameras in early-childhood settings, this skill analyzes children’s social interactions and produces pairwise frequency and duration statistics with a social-interaction report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Teachers and early-childhood staff can use the skill to review interaction patterns in classroom or play-area video and consult structured summaries as educational observations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Processing may involve uploading sensitive video of children, and the scan summary says task-specific authorization is unclear.

Mitigation: Obtain guardian and institution authorization before processing; limit access to recordings and reports, protect them, and retain them only as needed.

Risk: Account or credential handling is not clearly tied to the skill’s stated analysis purpose.

Mitigation: Use an authorized, trusted service configuration and restrict credentials to the people and systems that need them.

Risk: Interaction summaries or low-interaction flags could be mistaken for a developmental or mental-health assessment.

Mitigation: Use results only as educational observations; do not diagnose from them, and refer developmental concerns to qualified professionals.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/18072937735/skills/smyx-child-social-interaction-analysis-analysis)
- [API interface notes](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured interaction report with counts, durations, initiator summaries, heatmap or report links; Markdown report listings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May identify low-interaction candidates; results are visual behavior summaries, not diagnoses.]

## Skill Version(s):

1.0.19 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
