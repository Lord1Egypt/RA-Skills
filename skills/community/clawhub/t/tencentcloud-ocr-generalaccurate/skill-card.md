## Description: <br>
TencentCloud GeneralAccurate OCR calls Tencent Cloud's GeneralAccurateOCR service to extract high-accuracy text from images or single-page PDFs, with optional word-level details and resume-structure guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zt1314p-design](https://clawhub.ai/user/zt1314p-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract OCR text from images, URLs, Base64 image input, and single-page PDFs through Tencent Cloud OCR. It also provides guidance for turning OCR output from multilingual resumes into structured Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documents, resume contents, and other extracted text may include confidential or personal information and may be sent to Tencent Cloud OCR. <br>
Mitigation: Use the skill only with permission for the documents being processed, minimize or redact sensitive fields where possible, and follow the organization's data-handling requirements for Tencent Cloud services. <br>
Risk: The skill requires Tencent Cloud API credentials. <br>
Mitigation: Use scoped Tencent Cloud keys, provide them through environment variables, rotate them regularly, and avoid sharing keys in prompts, logs, or generated output. <br>
Risk: OCR and downstream resume parsing can produce incorrect or uncertain text. <br>
Mitigation: Review OCR output and any structured Markdown before using it for legal, hiring, identity, or other high-impact decisions. <br>


## Reference(s): <br>
- [Tencent Cloud GeneralAccurateOCR API documentation](https://cloud.tencent.com/document/api/866/37831) <br>
- [Multilingual resume parsing guidance](references/resume-parsing.md) <br>
- [ClawHub skill page](https://clawhub.ai/zt1314p-design/tencentcloud-ocr-generalaccurate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON OCR response with raw_text and RequestId; Markdown guidance for resume parsing output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports image URL or Base64 input, optional single-page PDF recognition, optional word-level output, and Tencent Cloud region selection.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
