## Description: <br>
Year-end tax package preparation pipeline for QBO-connected clients that generates a 9-tab Excel workbook covering tax summary, income, expenses, depreciation, 1099s, state nexus, crypto, checklist, and CDC outputs with IRS form and schedule mapping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Accountants, finance operators, and tax preparers use this skill to prepare year-end QBO-connected tax package materials for CPA review, including IRS line mapping, 1099 vendor checks, state nexus flags, crypto and FBAR indicators, and carryforward review prompts. The output supports review workflows and is not itself a filed tax return. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to run a local pipeline against sensitive QBO and client tax data without enough credential-scope guidance. <br>
Mitigation: Review the referenced pipeline in the user's workspace before execution and confirm the QBO token is scoped to the intended client, preferably read-only. <br>
Risk: Generated workbooks and CDC cache files can contain confidential client tax information. <br>
Mitigation: Store, restrict access to, or delete generated files according to client confidentiality and retention requirements. <br>
Risk: Tax mappings and checklist flags can be incomplete or misleading if source data, SOP signals, or prior-year return data are missing. <br>
Mitigation: Treat the workbook as preparation material only and require CPA or tax preparer review before using it for filing decisions. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/samledger67-dotcom/tax-package-prep) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with bash commands and generated Excel workbook files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a 9-tab Excel workbook and CDC cache; generated workbooks and cache files may contain sensitive client tax data and require CPA or tax preparer review before filing decisions.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
