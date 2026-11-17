## Description:

Verifies Vietnamese invoices by extracting invoice fields from PDF or image files and checking invoice existence and status through Vietnam e-invoice services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuwei19820201](https://clawhub.ai/user/liuwei19820201)

### License/Terms of Use:

MIT-0

## Use Case:

External users and finance or operations teams use this skill to extract key fields from Vietnamese invoice PDFs or images and check whether an invoice exists, is active, has been cancelled, or has another status condition.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoice content and related business data may be sent to named external services.

Mitigation: Install only with user consent for that data sharing and document which services receive invoice images, extracted fields, and captcha data.

Risk: The server security summary reports insecure network and logging practices.

Mitigation: Require TLS verification, redact logs, and avoid storing invoice contents or service credentials in command output before production use.

Risk: Authenticity results may be incomplete if extracted fields are wrong or not validated against the official record.

Mitigation: Treat results as advisory until material invoice fields are reviewed and matched against the official response.

Risk: Runtime dependencies and external browser automation increase operational exposure.

Mitigation: Pin and review dependencies, isolate the execution environment, and keep Playwright browser components current.

## Reference(s):

- [Vietnam invoice field extraction reference](artifact/references/invoice_fields.md)
- [Vietnam e-invoice service endpoint](https://hoadondientu.gdt.gov.vn:30000)
- [Alibaba Cloud Bailian console](https://bailian.console.aliyun.com)
- [DashScope OpenAI-compatible API endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1)
- [Chaojiying captcha service](https://www.chaojiying.com)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON verification result with a human-facing Markdown summary and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include invoice authenticity status, existence status, invoice status, processing status, detail text, extracted fields, and raw service response data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
