## Description:

A management assistant for solo Traditional Chinese Medicine practitioners that helps maintain Excel-based patient records, medical charts, herbal inventory, appointments, and billing reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[slamw](https://clawhub.ai/user/slamw)

### License/Terms of Use:

MIT-0

## Use Case:

External practitioners and clinic operators use this skill for day-to-day solo TCM clinic administration, including patient intake, charting, prescription support records, herbal stock tracking, appointment scheduling, and billing summaries. It is not positioned for academic TCM theory, formula research, or herb pharmacology analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles patient health and billing records with weak built-in privacy safeguards.

Mitigation: Use only on a secured single-user machine or protected clinic environment, and add privacy, access-control, encryption, retention, and backup safeguards before using it for regulated clinical records.

Risk: Excel files and command output may contain sensitive patient health and billing information.

Mitigation: Keep the data directory out of shared, synced, public, or source-controlled folders, and treat generated files and agent-visible command output as sensitive.

Risk: Spreadsheet-based workflows may need formula-sanitization safeguards when handling untrusted input.

Mitigation: Add spreadsheet-formula sanitization before importing, sharing, or processing untrusted patient, inventory, appointment, or billing values.

## Reference(s):

- [TCM Clinic Data Table Schema Reference](references/data-schema.md)
- [TCM Clinic - English Edition on ClawHub](https://clawhub.ai/slamw/skills/tcm-clinic-en)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown tables and summaries with CLI commands and local Excel workbook updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local .xlsx files under clinic_data; dates use YYYY-MM-DD and amounts use two decimal places.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
