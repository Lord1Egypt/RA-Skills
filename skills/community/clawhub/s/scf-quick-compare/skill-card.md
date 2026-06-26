## Description: <br>
Period-over-period variance analysis on the Statement of Cash Flows pulled from QuickBooks Online, producing a four-tab Excel workbook with summary, detail, flags, and CDC log views. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Accountants, finance teams, and agents supporting client close workflows use this skill to compare QuickBooks Statement of Cash Flows periods and produce a variance workbook with summary, detail, flags, and CDC log tabs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Excel reports and the local CDC cache may contain sensitive client financial data. <br>
Mitigation: Use the skill only in a trusted workspace, limit QuickBooks access to the intended company, and delete or protect generated reports and .cache/scf-quick-compare data when no longer needed. <br>
Risk: The skill depends on a referenced local Python pipeline and QuickBooks credentials that are not included in the artifact. <br>
Mitigation: Verify the referenced script and QuickBooks configuration before use, and scope credentials to the intended QuickBooks company. <br>


## Reference(s): <br>
- [SCF Quick Compare on ClawHub](https://clawhub.ai/samledger67-dotcom/scf-quick-compare) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with bash command examples; the referenced pipeline writes an Excel workbook.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Workbook output includes Summary, Detail, Flags, and CDC Log tabs; repeated runs may use a local .cache/scf-quick-compare cache.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
