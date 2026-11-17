## Description:

B2B company research producing professional PDF reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomstools11](https://clawhub.ai/user/tomstools11)

### License/Terms of Use:


## Use Case:

External users, sales teams, and business-development analysts use this skill to research a company from its URL, structure the findings, and generate a professional PDF account research report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated company research may contain incorrect, incomplete, or outdated claims if public sources are limited.

Mitigation: Verify important claims, citations, and links before relying on or sharing the report.

Risk: Temporary JSON inputs and generated PDFs may contain sensitive company, prospect, or lead-generation data.

Mitigation: Review where temporary data and final PDFs are written, restrict access to saved reports, and clean up sensitive research data after use.

Risk: Installing ReportLab at runtime can introduce dependency uncertainty.

Mitigation: Use a pinned or preinstalled ReportLab dependency in controlled environments.

## Reference(s):

- [Report Data Schema](references/data-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with JSON research data, shell commands, and a generated PDF file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a local PDF report from structured company research data; important claims and links should be verified before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
