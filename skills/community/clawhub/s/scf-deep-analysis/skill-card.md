## Description:

SCF Deep Analysis performs controller-level Statement of Cash Flows analysis for QBO-connected clients, computing cash-flow quality, free cash flow, working-capital drivers, rolling averages, GL drill-downs, controller findings, and a 7-tab Excel workbook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Accounting and finance teams use this skill during monthly close, board preparation, and internal review to explain cash-flow changes for QBO-connected clients and identify AR, AP, inventory, prepaid, capex, and material variance drivers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: QBO access and dependency installation are part of the workflow.

Mitigation: Run the skill only in a trusted accounting environment and prefer a virtual environment with pinned dependencies.

Risk: Generated workbooks and `.cache/scf-deep-analysis/{slug}.json` can contain sensitive client financial data.

Mitigation: Apply appropriate local access controls and clean up generated workbooks and cache files on shared machines.

Risk: Controller findings and action proposals may influence accounting or finance decisions.

Mitigation: Review findings with qualified finance personnel and preserve the skill's audit disclaimer in generated workbooks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samledger67-dotcom/skills/scf-deep-analysis)

## Skill Output:

**Output Type(s):** [Analysis, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with shell command examples and an Excel workbook output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a 7-tab Excel workbook and may update a local per-client cache used for change tracking.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
