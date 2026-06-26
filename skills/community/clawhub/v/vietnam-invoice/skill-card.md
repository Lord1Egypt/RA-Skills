## Description: <br>
Verifies Vietnamese invoices by extracting invoice fields from PDF or image files and checking them against the Vietnam tax authority API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuwei19820201](https://clawhub.ai/user/liuwei19820201) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and finance operations teams use this skill to inspect Vietnamese invoice PDFs or images, extract required invoice fields, and receive an authenticity result with invoice status details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invoice documents or extracted invoice details are sent to configured external VL and CAPTCHA services. <br>
Mitigation: Use the skill only with approved providers, dedicated low-privilege credentials, and invoice data that may be shared with those services. <br>
Risk: The security summary flags disabled TLS verification for tax-authority requests. <br>
Mitigation: Run the skill in an isolated environment and review the TLS verification behavior before relying on results for business decisions. <br>
Risk: The skill requires secret values for the VL provider and CAPTCHA service. <br>
Mitigation: Provide secrets through environment variables, avoid pasting them into chat or logs, and rotate credentials if exposure is suspected. <br>


## Reference(s): <br>
- [Vietnam invoice field extraction reference](references/invoice_fields.md) <br>
- [ClawHub release page](https://clawhub.ai/liuwei19820201/vietnam-invoice) <br>
- [Chaojiying CAPTCHA service](https://www.chaojiying.com) <br>
- [Alibaba Cloud Bailian console](https://bailian.console.aliyun.com) <br>
- [DashScope compatible API endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1) <br>
- [Vietnam electronic invoice API endpoint](https://hoadondientu.gdt.gov.vn:30000) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON verification results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide dependency installation and environment variable setup before producing invoice authenticity results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
