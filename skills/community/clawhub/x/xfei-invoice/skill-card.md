## Description: <br>
Recognize and extract structured data from invoices, receipts, and bills using iFlytek OCR API (科大讯飞票据识别). Supports VAT invoices, taxi receipts, train tickets, toll invoices, medical bills, bank receipts, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qingzhe2020](https://clawhub.ai/user/qingzhe2020) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and expense-workflow users use this skill to submit invoice, receipt, and bill images to iFlytek OCR and extract structured fields for review or automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Troubleshooting commands may print XFEI_API_KEY or XFEI_API_SECRET values to the terminal. <br>
Mitigation: Use presence-only or masked environment-variable checks, and do not run or share commands that echo full API secrets. <br>
Risk: Invoice and bill images are sent to the iFlytek OCR service for processing. <br>
Mitigation: Use the skill only for documents the user is comfortable sending to iFlytek, and confirm organizational data-handling requirements before processing sensitive invoices. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qingzhe2020/xfei-invoice) <br>
- [iFlytek console](https://console.xfyun.cn) <br>
- [iFlytek invoice recognition service](https://www.xfyun.cn/services/Invoice_recognition?target=price) <br>
- [iFlytek invoice OCR API endpoint](https://api.xf-yun.com/v1/private/sc45f0684) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown guidance with shell command examples; the script outputs human-readable text or raw JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires XFEI_APP_ID, XFEI_API_KEY, and XFEI_API_SECRET environment variables and a local invoice or receipt image path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
