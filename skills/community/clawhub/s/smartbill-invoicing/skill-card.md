## Description: <br>
Issue SmartBill invoices through the SmartBill.ro API with local automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Maverick-AI-Tech](https://clawhub.ai/user/Maverick-AI-Tech) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, finance operators, and agent users use this skill to validate SmartBill invoice payloads, create draft or final invoices, list configured document series, and download invoice PDFs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses SmartBill credentials and handles invoice and customer data. <br>
Mitigation: Install only where that access is acceptable, provide credentials through the documented environment variables, and avoid exposing generated payloads or responses. <br>
Risk: Creating a final invoice is a high-impact financial action. <br>
Mitigation: Run validation and dry-run first, then use the final-invoice flag only after explicit user confirmation. <br>
Risk: Debug logging can expose invoice payloads or SmartBill responses. <br>
Mitigation: Keep debug mode disabled unless logs are protected and the operator is prepared for invoice data to appear there. <br>
Risk: Invoice PDF downloads write files to a user-selected path. <br>
Mitigation: Choose PDF output paths deliberately and keep them within the working directory or an allowed media root. <br>


## Reference(s): <br>
- [SmartBill API Notes](references/smartbill-api.md) <br>
- [Invoice Example](references/invoice-example.json) <br>
- [SmartBill API Base URL](https://ws.smartbill.ro/SBORO/api) <br>
- [ClawHub Skill Page](https://clawhub.ai/Maverick-AI-Tech/smartbill-invoicing) <br>
- [Publisher Profile](https://clawhub.ai/user/Maverick-AI-Tech) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON, files] <br>
**Output Format:** [Markdown guidance with inline shell commands; CLI output is JSON and downloaded invoices are PDF files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SmartBill credentials and python3; final invoice creation requires an explicit allow-final flag.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
