## Description: <br>
United States federal income tax filing assistant for US citizens, resident aliens, and nonresident aliens that guides filer classification, form routing, amount calculations, IRS PDF form filling, and cross-form validation for federal returns only. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Irreel](https://clawhub.ai/user/Irreel) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and tax-preparation agents use this skill to prepare US federal income tax returns, determine resident or nonresident filing workflows, identify required IRS forms and schedules, fill IRS PDFs with pypdf, and validate totals across forms. <br>

### Deployment Geography for Use: <br>
Global access for United States federal tax filing workflows only. <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for highly sensitive tax, residency, travel-history, and immigration information. <br>
Mitigation: Use it only for explicit tax-preparation tasks, redact full identifiers where possible, and share only the minimum documents or fields needed for the workflow. <br>
Risk: The security review notes that the skill may activate too broadly for general tax-related mentions. <br>
Mitigation: Confirm the user wants US federal tax-preparation help before collecting documents or applying filing workflows. <br>
Risk: Incorrect tax routing, calculations, treaty handling, or PDF field updates can produce inaccurate returns or corrupted PDFs. <br>
Mitigation: Cross-check generated forms against source documents, review treaty and filing-status decisions with a qualified professional when uncertain, and use the bundled safe PDF updater without overwriting the input file. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Irreel/tax-filing) <br>
- [Filing status decision tree](references/filing-status.md) <br>
- [Form routing tables](references/form-routing.md) <br>
- [Common schedules reference](references/common-schedules.md) <br>
- [Form field mappings](references/form-field-maps.md) <br>
- [pypdf recovery guidance](references/pypdf-recovery.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Files] <br>
**Output Format:** [Markdown with tables, checklists, inline Python and bash snippets, and PDF form update instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or modify IRS PDF files through the bundled pypdf script; no API keys or credential environment variables were detected.] <br>

## Skill Version(s): <br>
0.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
