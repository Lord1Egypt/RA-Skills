## Description:

Exports multi-dimensional WeChat Channels customer data reports for a named customer by calling an internal API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahsbnb](https://clawhub.ai/user/ahsbnb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and authorized internal operators use this skill to export WeChat Channels data for a named customer and pass the generated report to downstream analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exports sensitive customer data from an internal system.

Mitigation: Install only where users are authorized to export the named customers' data, require explicit confirmation before each export, and treat generated spreadsheets and reports as confidential.

Risk: Under-scoped access and unsafe local file handling could expose or misplace exported customer data.

Mitigation: Validate client identifiers, restrict network access to the approved backend, sanitize filenames, and review the output directory before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ahsbnb/skills/wechat-data-exporter)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands]

**Output Format:** [XLSX files, a JSON summary report, and console status text including a REPORT_PATH line]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated exports and reports may contain confidential customer data and should be handled accordingly.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
