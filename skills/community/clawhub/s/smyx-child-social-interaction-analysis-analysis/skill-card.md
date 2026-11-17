## Description:

Analyzes fixed-camera video from early education settings to summarize children's social interactions and generate reports and heatmaps for educators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Teachers and early education staff use the reports to review pairwise interaction frequency, duration, and initiators, and to guide classroom support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags uncertainty about what video and identity data are sent, who receives it, and whether export-only use may still trigger analysis; scan coverage is incomplete.

Mitigation: Before use, verify the data flow, recipient, and export-only behavior. Follow the skill's guidance to obtain guardian or school consent and protect recordings.

Risk: Interaction estimates and low-interaction flags can be unreliable when camera coverage or distance calibration is inadequate, and may be mistaken for a clinical assessment.

Mitigation: Use a stable view that covers the activity area, provide calibration where available, and treat results as educational reference rather than diagnosis.

## Reference(s):

- [API documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release](https://clawhub.ai/18072937735/skills/smyx-child-social-interaction-analysis-analysis)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON]

**Output Format:** [Structured interaction report in Markdown or JSON, with report and heatmap links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes pairwise interaction counts and durations, initiator statistics, heatmap links, and low-interaction candidates.]

## Skill Version(s):

1.0.17 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
