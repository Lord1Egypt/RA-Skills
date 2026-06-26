## Description: <br>
Receipt Assistant helps process reimbursement receipts by recognizing common receipt types, extracting dates, amounts and invoice details, applying standardized file names, and generating an Excel summary report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YY-C8](https://clawhub.ai/user/YY-C8) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, finance staff, and administrative users can use this skill to organize reimbursement receipt files, extract key receipt fields, rename files consistently, and produce an Excel reimbursement summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Receipt images and PDFs may contain personal, travel, tax, or reimbursement information. <br>
Mitigation: Process only folders intentionally selected by the user and review generated filenames and reports before sharing them. <br>
Risk: Generated receipt fields, filenames, or Excel summaries may be inaccurate if visual recognition or user-provided data is wrong. <br>
Mitigation: Verify extracted dates, amounts, invoice numbers, sellers, and passenger names against the original receipts before submission. <br>
Risk: Untrusted receipt files and unpinned dependencies can increase local processing risk. <br>
Mitigation: Use a sandboxed or pinned-dependency environment when processing untrusted files. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, shell commands, files] <br>
**Output Format:** [Markdown guidance, JSON-style extracted fields, standardized filenames, and Excel workbook files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes user-selected PDF, JPG, PNG, and JPEG receipt files; generated outputs should be reviewed before sharing.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
