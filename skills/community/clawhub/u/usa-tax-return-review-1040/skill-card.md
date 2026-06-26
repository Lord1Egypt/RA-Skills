## Description: <br>
Reviews U.S. individual income tax returns for Form 1040/1040-SR, checks current-year tax rules and multi-year consistency, and produces findings, a summary, a DOCX risk register, and an audit-likelihood estimate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChipmunkRPA](https://clawhub.ai/user/ChipmunkRPA) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Tax preparers, reviewers, and finance teams use this skill to run structured risk and consistency reviews of normalized U.S. Form 1040 data before human professional review. It is intended to surface compliance signals, documentation needs, and audit-risk indicators, not to make final filing or legal determinations. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports can contain sensitive tax-return data. <br>
Mitigation: Run the skill in a private local directory, avoid cloud-synced or shared output folders, restrict file permissions where possible, use --skip-docx when a Word report is not needed, and delete generated reports when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ChipmunkRPA/usa-tax-return-review-1040) <br>
- [Publisher profile](https://clawhub.ai/user/ChipmunkRPA) <br>
- [Input schema](references/input_schema.json) <br>
- [Current tax law parameters](references/current_tax_law_2025.json) <br>
- [Major items reference](references/major_items_reference.md) <br>
- [IRS federal income tax rates and brackets](https://www.irs.gov/filing/federal-income-tax-rates-and-brackets) <br>
- [IRS Publication 501](https://www.irs.gov/publications/p501) <br>
- [IRS Child Tax Credit](https://www.irs.gov/credits-deductions/individuals/child-tax-credit) <br>
- [SSA contribution and benefit base](https://www.ssa.gov/oact/COLA/cbbdet.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON findings, Markdown summary, DOCX risk register, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local reports that may contain sensitive tax information; DOCX output can be skipped with --skip-docx.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
