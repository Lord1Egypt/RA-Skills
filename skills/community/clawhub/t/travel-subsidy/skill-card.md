## Description:

When the user uploads 发票.zip and 火车票.zip, use the included data tables to calculate eligible business-trip subsidy records, split related vs remaining files, create output workbooks, package two result zips, and report progress at every key step.

This skill is ready for commercial/non-commercial use.

## Publisher:

[attorneytao](https://clawhub.ai/user/attorneytao)

### License/Terms of Use:


## Use Case:

Employees and finance operations users can use this skill to process Chinese invoice and train-ticket archives for business-trip subsidy calculation. It organizes eligible supporting records separately from remaining files and creates reviewable workbooks and zip packages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow reads and reorganizes potentially sensitive travel and financial records.

Mitigation: Use it only with the intended invoice and train-ticket archives, keep processing local, and restrict access to generated spreadsheets and zip files.

Risk: Generated subsidy totals and eligibility decisions may affect reimbursement outcomes.

Mitigation: Review the generated workbooks, unresolved cases, and excluded-record reasons before relying on the totals.

Risk: Uploaded archives and filenames are untrusted inputs.

Mitigation: Extract only into a dedicated run directory, protect against path traversal, and do not execute extracted files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/attorneytao/skills/travel-subsidy)
- [Publisher profile](https://clawhub.ai/user/attorneytao)

## Skill Output:

**Output Type(s):** [Files, Text, Guidance]

**Output Format:** [Two zip archives containing XLSX workbooks and organized ticket/invoice files, plus visible progress and summary text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes local uploaded archives and writes outputs under a dedicated run directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
