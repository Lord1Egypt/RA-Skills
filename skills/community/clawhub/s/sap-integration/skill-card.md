## Description:

SAP Integration Suite supports SAP ABAP, HANA, and S/4HANA integration through data extraction, RFC/BAPI calls, API integration, ABAP generation, table analysis, workflow automation, and migration guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[highlander89](https://clawhub.ai/user/highlander89)

### License/Terms of Use:


## Use Case:

Developers, SAP administrators, and integration engineers use this skill to plan and perform SAP data extraction, RFC/BAPI calls, API integration, ABAP development support, workflow automation, and S/4HANA migration tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad SAP RFC and table-access capabilities can expose or change sensitive enterprise data if installed for broad users.

Mitigation: Install only for authorized SAP administrators or developers, use least-privilege SAP accounts, and restrict which tables and functions can be used.

Risk: Local JSON or Excel exports can contain sensitive SAP business data.

Mitigation: Protect credential and configuration files, and treat exported files as sensitive enterprise data with controlled storage and sharing.

Risk: Production SAP use can affect business systems without proper approval.

Mitigation: Use controlled SAP environments and require change approval before production operations.

## Reference(s):

- [SAP HANA Integration Guide](references/hana-integration.md)
- [S/4HANA Migration Guide](references/s4hana-migration.md)
- [SAP Enhancement Framework Guide](references/enhancement-framework.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code snippets, JSON examples, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local JSON or Excel export guidance when using the bundled scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
