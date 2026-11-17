## Description:

Generates and decodes QR codes using the CaoLiao QR Code API and local libraries for text, URL, image, and batch workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hinisal](https://clawhub.ai/user/hinisal)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate static QR codes, save QR images, decode QR contents from local files or URLs, and process QR data in batches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: QR contents and local QR images can be sent to api.2dcode.biz during generation or decode fallback.

Mitigation: Avoid confidential QR data, prefer local generation and decoding when possible, and manually control remote fallback for sensitive files.

Risk: The skill can automatically install Python or Node.js dependencies.

Mitigation: Install dependencies yourself in an isolated environment, review package manifests, and pin versions before deployment.

Risk: Batch decode can write results back into CSV or spreadsheet inputs.

Mitigation: Back up source spreadsheets before use and request TXT output when the original file should remain unchanged.

## Reference(s):

- [CaoLiao QR Code API documentation](https://cli.im/open-api/qrcode-api/quick-start.html)
- [QR Code API reference](reference.md)
- [qr-scanner-wechat](https://github.com/antfu/qr-scanner-wechat)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Files, JSON, Guidance]

**Output Format:** [Markdown responses with QR links and previews, JSON script results, and generated image, TXT, ZIP, CSV, or spreadsheet files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call CaoLiao API; decode fallback can upload local images; batch decode can modify CSV/XLSX inputs unless TXT output is requested.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
