## Description:

TencentCloud GeneralAccurate OCR helps agents extract text from images and single-page PDFs with Tencent Cloud OCR, and includes guidance for formatting multilingual resume OCR results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zt1314p-design](https://clawhub.ai/user/zt1314p-design)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to run Tencent Cloud GeneralAccurateOCR on images, URLs, Base64 input, and single-page PDFs, then return extracted text or format resume OCR text into readable Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images, PDFs, and resume contents are sent to Tencent Cloud OCR and may contain sensitive personal or business information.

Mitigation: Use the skill only with documents you are authorized to process, avoid highly sensitive inputs when possible, and redact outputs before sharing.

Risk: The skill depends on Tencent Cloud credentials and the Tencent Cloud Python SDK.

Mitigation: Store credentials in environment variables or a managed secret store, and pin and review the SDK dependency in controlled environments.

## Reference(s):

- [Tencent Cloud GeneralAccurateOCR API documentation](https://cloud.tencent.com/document/api/866/37831)
- [Multilingual resume parsing reference](references/resume-parsing.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON OCR results and Markdown-formatted resume summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Tencent Cloud request IDs and optional word-level OCR details.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
