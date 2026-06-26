## Description: <br>
Automates travel-expense reimbursement by finding invoice emails, downloading invoice PDFs from attachments or links, extracting invoice and itinerary data, and preparing FOL invoice upload and reimbursement submission steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sangjie123](https://clawhub.ai/user/sangjie123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees or finance operations users use this skill to collect travel invoices from email, parse invoice and itinerary details, summarize reimbursable expenses, and support upload and submission through the FOL reimbursement workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access mailbox contents, invoice PDFs, and travel details that may contain sensitive personal and financial data. <br>
Mitigation: Use a constrained mailbox or search scope where possible, review selected emails and invoices before processing, and remove temporary reimbursement files after completion. <br>
Risk: The skill may open invoice links or download files from email using curl or browser automation. <br>
Mitigation: Check sender identity and link domains before download, avoid untrusted links, and use manual PDF upload when a link requires login, captcha, or looks suspicious. <br>
Risk: The skill can upload invoices and submit reimbursement forms in FOL with limited explicit approval gates. <br>
Mitigation: Require user confirmation of invoice list, amounts, itinerary, project name, and reimbursement reason before any upload or form submission. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sangjie123/travel-expense-reimbursement) <br>
- [Travel reimbursement flowchart](references/flowchart.md) <br>
- [OCR invoice parsing guide](references/ocr-guide.md) <br>
- [Invoice URL downloader helper](references/url_downloader.py) <br>
- [Itinerary analysis guide](references/行程分析指南.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, JSON invoice data, generated reimbursement files, file paths, and shell or Python command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include invoice tables, itinerary summaries, total amounts, processing status, and manual fallback guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
