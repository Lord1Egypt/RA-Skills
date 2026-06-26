## Description: <br>
Controller-level Statement of Cash Flows deep analysis for QBO-connected clients that computes cash-flow quality, free cash flow, working-capital movement drivers, rolling averages, GL drill-down for flagged accounts, and controller findings with urgency-ranked action proposals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance and accounting teams use this skill during monthly close, board preparation, and internal cash-flow reviews to analyze QBO-connected Statement of Cash Flows data and explain material cash movement drivers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow relies on a separate scf-deep-analysis.py script that was not included in the artifact evidence. <br>
Mitigation: Inspect and trust the local script before running it, and confirm that it only performs the expected read-only report pulls. <br>
Risk: The skill processes sensitive QuickBooks financial data and writes generated Excel workbooks and cache files. <br>
Mitigation: Limit access to the output workbook and .cache/scf-deep-analysis contents, and handle them as sensitive financial records. <br>
Risk: A broadly scoped QBO token could expose more client data than the analysis requires. <br>
Mitigation: Use a read-only QBO token limited to the intended client and environment before executing the pipeline. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samledger67-dotcom/scf-deep-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, shell commands, files, guidance] <br>
**Output Format:** [Markdown instructions with bash command examples; the referenced pipeline produces a 7-tab Excel workbook.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a QBO-connected client slug, period arguments or YTD mode, a configured QBO auth token, openpyxl, and Node.js.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
