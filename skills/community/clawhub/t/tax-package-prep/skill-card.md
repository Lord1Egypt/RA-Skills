## Description:

Year-end tax package preparation pipeline for QBO-connected clients that generates a 9-tab Excel workbook and maps line items to IRS form and schedule codes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

External accounting and tax-preparation teams use this skill to turn full-year QBO data and client SOP signals into a CPA-reviewable year-end tax package workbook. It supports income and expense schedules, 1099 vendor review, depreciation checks, crypto and FBAR flags, state nexus indicators, checklist status, and year-over-year change tracking.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The workflow handles confidential client tax and financial records from QBO and client SOP files.

Mitigation: Install and run it only in environments approved for confidential tax records, with QBO access limited to the permissions needed for the client workflow.

Risk: Generated workbooks and .cache/tax-package-prep snapshots can persist sensitive financial data on local storage.

Mitigation: Use a secured output directory, avoid shared Desktop locations, and apply retention and deletion controls to generated workbooks and cache snapshots.

Risk: The workbook is tax-package support material, not a filed tax return.

Mitigation: Require CPA or tax preparer review before any filing decisions, especially for 1099s, state nexus, crypto, FBAR, depreciation, and carryforward items.

Risk: Some deductions and entity-specific items depend on records the pipeline cannot calculate or retrieve on its own.

Mitigation: Collect and verify mileage logs, home office square footage, prior-year returns, K-1 or basis details, and other missing documentation before treating checklist items as complete.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/samledger67-dotcom/skills/tax-package-prep)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Files, Guidance]

**Output Format:** [Markdown guidance with bash commands and a generated Excel workbook]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a 9-tab .xlsx tax package and may write local .cache/tax-package-prep snapshots for year-over-year comparisons.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
