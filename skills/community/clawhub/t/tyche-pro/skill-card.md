## Description:

Generates invoice and revenue reporting from CSV data, including multi-currency tracking, tax and late-fee calculations, reminder email drafts, project grouping, aged receivables, and analytics exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway)

### License/Terms of Use:

MIT-0

## Use Case:

Freelancers, small businesses, and billing operations users use this skill to turn invoice CSV data into local invoice status reporting, payment reminder drafts, aged receivables, project revenue grouping, and analytics exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags setup and export behavior for review before use.

Mitigation: Review the skill before installing, use a virtual environment rather than the provided system-level pip command, and avoid running setup as an administrator.

Risk: Generated reports and analytics CSVs can contain sensitive billing data.

Mitigation: Store generated files only in a private folder and handle exported CSVs as sensitive billing records.

Risk: Invoice data from untrusted sources can flow into generated reports and exports.

Mitigation: Open exports only from invoice data you control or have reviewed.

## Reference(s):

- [Tyche Pro ClawHub page](https://clawhub.ai/occupythemilkyway/skills/tyche-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash and Python code blocks; generated Markdown report and CSV analytics export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LICENSE_KEY; optional invoice CSV and billing environment variables; runs locally and writes dated report and analytics files.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
