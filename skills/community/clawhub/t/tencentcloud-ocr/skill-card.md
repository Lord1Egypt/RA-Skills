## Description:

TencentCloud OCR calls Tencent Cloud GeneralAccurateOCR to extract text from images, image URLs, and single-page PDFs, with optional word-level details and resume parsing guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zt1314p-design](https://clawhub.ai/user/zt1314p-design)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run Tencent Cloud GeneralAccurateOCR on user-provided images, image URLs, and PDFs, then return extracted text or structured resume summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted images, PDFs, URLs, and resume contents may be processed by Tencent Cloud using the installer's Tencent Cloud OCR credentials.

Mitigation: Install only where Tencent Cloud processing is approved, avoid highly sensitive documents unless authorized, and require explicit user confirmation before OCR runs on attachments or links.

Risk: Overbroad cloud credentials could expose more Tencent Cloud permissions than this OCR workflow requires.

Mitigation: Use least-privilege OCR-only Tencent Cloud credentials stored in TENCENTCLOUD_SECRET_ID and TENCENTCLOUD_SECRET_KEY.

Risk: The Tencent Cloud SDK dependency may change behavior if installed without version control.

Mitigation: Pin tencentcloud-sdk-python in the runtime environment and review updates before deployment.

## Reference(s):

- [Tencent Cloud GeneralAccurateOCR API documentation](https://cloud.tencent.com/document/api/866/37831)
- [Resume parsing guidance](references/resume-parsing.md)
- [Tencent Cloud API key management](https://console.cloud.tencent.com/cam/capi)
- [Tencent Cloud OCR purchase page](https://buy.cloud.tencent.com/iai_ocr)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON OCR results and Markdown resume summaries, with setup guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [OCR output includes raw_text and RequestId; no-text results include an explanatory message.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
