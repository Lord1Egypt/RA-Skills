## Description: <br>
Vendor Compliance 1099 helps accounting firms run year-end 1099 compliance by aggregating QBO general ledger vendor payments, applying IRS thresholds and classifications, tracking W-9 and TIN status, and producing an 8-tab Excel workbook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Accounting firms and tax staff use this skill for year-end 1099 vendor compliance runs, W-9 tracking, IRS threshold checks, and review of vendor payment classifications before filing. It is not intended for payroll W-2, 1042-S foreign withholding, 1099-K reconciliation, state-level 1099 filing, or non-US entities. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: The workflow handles sensitive client accounting and tax records in generated workbooks and cache files. <br>
Mitigation: Restrict access to outputs, store them according to client tax-record handling policies, and avoid sharing generated files outside approved accounting workflows. <br>
Risk: The reviewed artifact references a local Python pipeline that is not included in the artifact. <br>
Mitigation: Inspect and trust the referenced pipeline before running it, confirm dependencies are expected, and use a read-only QBO token scoped to the intended client. <br>
Risk: 1099 classifications, corporate exemptions, W-9 status, TIN status, and filing obligations can require professional review before tax filing. <br>
Mitigation: Review workbook tabs before relying on the results, verify entity types and vendor documentation, and confirm filing decisions with the responsible tax professional. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/samledger67-dotcom/vendor-compliance-1099) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands; generated pipeline output is an XLSX workbook and JSON cache files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces VendorCompliance_1099_{slug}_{year}.xlsx and local .cache/vendor-compliance-1099 state files.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
