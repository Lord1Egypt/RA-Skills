## Description:

Visit Management generates Excel-based customer visit plans, daily reminders, and follow-up summaries for property service teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perrykono-debug](https://clawhub.ai/user/perrykono-debug)

### License/Terms of Use:

MIT-0

## Use Case:

Property service employees and operations teams use this skill to generate weekly visit plans, daily reminders, visit quality summaries, and follow-up status from a trusted Excel workbook.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles and persists sensitive customer and business data through a fixed local workbook path and local output directories.

Mitigation: Install only in a controlled trusted deployment; require explicit approval for workbook access, restrict file permissions, and set retention limits for generated outputs and backups.

Risk: The skill can update visit records and generate operational notifications, which could affect customer follow-up workflows if run with untrusted inputs or destinations.

Mitigation: Require operator approval before sending notifications or updating visit records, and verify the workbook path, output directories, WeCom destination, and operators before production use.

Risk: Excel writes may preserve or introduce unsafe formulas when customer or visit data is exported.

Mitigation: Apply formula neutralization for Excel writes before production deployment.

## Reference(s):

- [Visit Management API Reference](artifact/references/api_reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown guidance with structured JSON plans, reminders, reports, and optional shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local Excel workbook as input and may create local JSON plan, reminder, report, and backup files.]

## Skill Version(s):

2.0.0 (source: server release metadata and SKILL.md version history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
