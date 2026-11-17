## Description:

Ticket Stats analyzes internal support ticket spreadsheets, counts received, resolved, and late-response tickets, classifies issues by business module, and generates daily summary reports with visual charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flankcat](https://clawhub.ai/user/flankcat)

### License/Terms of Use:

MIT-0

## Use Case:

Support operations teams and internal business analysts use this skill to analyze Excel or CSV ticket exports, classify issues by module, and produce daily ticket metrics, overdue-response details, and charts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Internal ticket files and generated reports can expose ticket IDs, issue descriptions, response timing, and support trends.

Mitigation: Run the skill only on ticket data the user is authorized to analyze, and restrict sharing of generated text reports and PNG charts.

Risk: Generated report and chart files may be written to an output directory that is not appropriate for sensitive operational data.

Mitigation: Choose a secure output directory before running the analysis and apply the same retention and access controls used for the source ticket data.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, code, shell commands, files, guidance]

**Output Format:** [Markdown guidance with Python and shell examples; generated TXT reports and optional PNG chart files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes local Excel or CSV ticket files with optional date and output directory arguments.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
