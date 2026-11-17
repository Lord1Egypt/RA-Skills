## Description:

Check data compliance with construction standards and validate data against ISO 19650, IFC, COBie, and UniFormat standards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction)

### License/Terms of Use:

MIT

## Use Case:

Developers, construction data teams, BIM managers, and project management assistants use this skill to check project records against construction data standards, summarize compliance status, and identify rule failures or warnings. It supports individual records, batches, and multiple standards for workflows involving ISO 19650, IFC, COBie, UniFormat, MasterFormat, and Omniclass.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read project data files and create exports through filesystem access.

Mitigation: Confirm intended file access scope before installation and use workspace permissions that limit the skill to the project data needed for the compliance check.

Risk: Custom validation rules can include patterns that may be unsafe or expensive if accepted from untrusted users.

Mitigation: Apply schema checks, pattern length limits, and regex execution safeguards before accepting third-party or user-supplied rules.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/datadrivenconstruction/skills/standards-compliance-checker)
- [DataDrivenConstruction Homepage](https://datadrivenconstruction.io)

## Skill Output:

**Output Type(s):** [text, markdown, code, files, guidance]

**Output Format:** [Markdown, structured tables, Python examples, and optional CSV, Excel, or JSON exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes compliance levels, pass/fail counts, warning counts, issue details, summary statistics, and suggested fixes.]

## Skill Version(s):

2.1.0 (source: server release metadata; artifact/claw.json lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
